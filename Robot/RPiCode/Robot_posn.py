# Robot_posn: - routine to track a fiducial tag using a turret mounted camera
# the robot and use to calculate the x,y (in arena coordinates) the position
# of the robot
#
# 28 Jun 2020; 0709: added turret slew logic
# 27 Jun 2020; 1559: inital starting point using code from 'Localization.py' 

from picamera import PiCamera
from time import sleep
import datetime
import apriltag
import cv2
import math
import time
import glob
import os
import sys
import signal
import logging
import schedule
import csv
import RPi.GPIO as GPIO
import pigpio

servo = 13

img_h = 1280  # image width in pixels
img_v = 1024  # image height in pixels
img_cx = 0.5 * img_h  # center pixel in x direction
img_cy = 0.5 * img_v  # center pixel in y direction

def signal_handler(sig, frame):
    print('ctrl-c detected')
    logging.info('ctrl-c detected')
    sys.exit(0)

def i_capture(name):
    file_name = "/home/pi/RPi-Ardunio/Robot/RPiCode/" + name + datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S.%f.jpg")
    camera.capture(file_name)
    #print('\n', file_name)
    logging.info('File name: {a}'.format (a=file_name))

def extract_center(result, i):
    # result (input): apriltag detection list/array
    # i (input): the ith detected tag
    # xcpx (output): x center coord (in px) of tag
    # ycpx (output): y center coord (in px) of tag
    xcpx = result[i].center[0]
    ycpx = result[i].center[1]
#    print("from def ", xcpx, "  ", ycpx)
    return xcpx, ycpx

def extract_corner(result, i):
    # result (input): apriltag detection list/array
    # i (input): the ith detected tag
    # ytlpx (output): y-coord (in px) of top left corner of tag
    # yllpx (output): y-coord (in px) of lower left corner of tag
    ytlpx = result[i].corners[0,1]
    yllpx = result[i].corners[3,1]
    return ytlpx, yllpx

def calc_range(obj_hgt, real_hgt):
    # set up constants:
    global img_h
    focal_len = 3.6  # camera focal length in mm
    image_hgt = img_h  # image height in px
    sensor_hgt = 2.74  # sensor height in mm
    # obj_hgt (input) in px
    # real_hgt (input) in mm
    # r_range is output in mm
    r_range = (focal_len * real_hgt * image_hgt)/(obj_hgt * sensor_hgt)
    return r_range

def readGndT(gndTfilename):
    with open(gndTfilename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        titles = next(csvreader)
    
        for target in csvreader:
            targets.append(target)
        
    logging.info('Targets read and returned: {a}'.format (a=targets))
    return targets

"""
= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
   Initialization and Setup
= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
"""

logging.basicConfig(filename="/home/pi/RPi-Ardunio/Robot/RPiCode/log_Robot_posn.log", level=logging.INFO, format='%(asctime)s %(message)s')
signal.signal(signal.SIGINT, signal_handler)
#schedule.every(0.5).seconds.do(i_capture,'track_i')

# insert parameters and constants

camera = PiCamera()
camera.resolution = (img_h, img_v)
# CSV file parameters
gndTfilename = "/home/pi/RPi-Ardunio/Robot/Input Files/gndTrth.csv"
titles = []
targets = []

xcpx = 0  # x(px) center of robot tag
ycpx = 0  # y(px) center of robot tag
ytlpx = 0  # y coor of top left px of robot tag
yllpx = 0  # y coor of lower left px of robot tag

# after capturing image and writing to file, this code picks up most recent file
# list_files = glob.glob('/home/pi/RPi-Ardunio/*.jpg')
# latest_file = max(list_files, key=os.path.getctime)
# print ("newest image file: ", latest_file)
# logging.info('Newest image file: {a}'.format (a=latest_file))

"""
= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
   Calibration
= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
"""
logging.info('Calibration start')
# read ground truth file with fiducial target parameters
targets = readGndT(gndTfilename)
logging.info('Targets from csv file: {a}'.format (a=targets))

camera.start_preview(fullscreen=False, window=(700,100,512,384))
sleep(2)  # give camera time to stablize

# slew turret to 90 degrees - pointed straight forward of robot
pwm = pigpio.pi()
pwm.set_mode(servo, pigpio.OUTPUT)
pwm.set_PWM_frequency(servo, 50)
print("90 degrees")
logging.info('90 degrees')
pwm.set_servo_pulsewidth(servo, 1500)
cur_az = 1500
stepsz = 5  # set pwm step size increment

l=0 # will loop and capture calibration images until tag 0 is in center
    # asks for input at end of loop enter either '0' loop again or non-zero
    # to continue with the program
while l==0:
    
    i_capture('calibration')
    list_files = glob.glob('/home/pi/RPi-Ardunio/Robot/RPiCode/*.jpg')
    cal_image = max(list_files, key=os.path.getctime)
    print ("calibration image file: ", cal_image)
    logging.info('Calibration image file: {a}'.format (a=cal_image))
    img = cv2.imread(cal_image,cv2.IMREAD_GRAYSCALE)

    detector = apriltag.Detector()

    result = detector.detect(img)
    if result == []:
        print ("Empty arrary - no targets found")
        logging.info('Empty array')
    else:
        for i in range(len(result)):
            # look for targets on robot(s) as of this writing apriltag #499
            if result[i].tag_id != 499:
                # call def to extract center x,y pixels
                xcpx, ycpx = extract_center(result, i)
                print('\n', "tag id= ", result[i].tag_id, "  target center: ", xcpx, "  ", ycpx)
               
                # call def to extract top left and lower left corner y pixels
                # only need the y-coord as calculating the height of the tag
                ytlpx, yllpx = extract_corner(result, i)
                print("left corners: ", ytlpx, "  ", yllpx)
                obj_hgt = int(yllpx - ytlpx)
                print("Fiducial target object height: ", obj_hgt)
                            
                # call def to calculate range to robot (def calc_range)
                              
                
                # scroll through the ground truth targets looking for a tag match
                for k in range(len(targets)):
                    #print('\n', 'k= ', k, ' targets tag= ',targets[k][0],' detected tag= ',result[i].tag_id, ' xcpx= ', xcpx)
                    if int(targets[k][0]) == int(result[i].tag_id):
                        # if gndT tag id matches detected tag id, write px coord to the list                 
                        targets[k][7] = int(xcpx)
                        targets[k][8] = int(ycpx)
                        r_hgt = float(targets[k][6])                       
                        r_range = calc_range(obj_hgt, r_hgt)
                        targets[k][9] = int(r_range)
                        print("Fiducial range: ", r_range)
                        logging.info('Fiducial target object height and range: {a}, {b}'.format (a=obj_hgt, b=r_range))

                
                logging.info('Detected tags added to list: {a}'.format (a=targets))
                
                # call def to estimate robot azimuth angle (def calc_az_angle)
                # call def to calculate robot x,y location in arena coordinates (def calc_rposn)
            
    #find fiducial tag 0 and extract range and x-coord
    for i in range(len(targets)):
        print('\n','looking for fiducial 0', 'i= ',i, ' targets[i][0]= ', targets[i][0])
        if int(targets[i][0]) == 0:
            
            tag0_r = targets[i][9]
            tag0_x = targets[i][7]
            print('\n', 'found fiducial tag 0; tag0_r: ', tag0_r)
    #calculate px/mm at the base target range 26.75 deg = .4669 rad
    pxmm = (2 * tag0_r * math.sin(.4669))/1280
    print('\n', 'pxmm: ', pxmm)
    
    #scroll through fiducial targets and calculate degree offset
    for k in range(len(targets)):
        dx = int(targets[k][7]) - int(tag0_x)
        print('\n', 'dx in px: ', dx)
        dx = dx*pxmm
        print('\n', 'dx in mm: ', dx)
        theta = math.asin(dx/tag0_r)
        degOset = round(math.degrees(theta),1)
        print('\n ', "dx: ", dx, ' degOffset: ', degOset)
        targets[k][10] = degOset
        
    logging.info('Fiducial targets list: {a}'.format (a=targets))       
    l = input("Press '0' for another image; '1' to continue: ")
    l = int(l)

"""
+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
    MAIN LOOP
+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
"""
while True:
    """    
    = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
   Image Capture
    = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    """
    
    lock = 0 #set lock switch to false to start the search and lock loop
    while (lock == 0):
        
        #camera.start_preview(fullscreen=False, window=(100,100,512,384))

        #schedule.every(1.0).seconds.do(i_capture,'track_i')
        
        #Use ctrl-c to terminate

        #schedule.run_pending()

        """
        = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
        Detect Robot(s) Targets
        = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
        """
        i_capture('Fid_tracking-')
        list_files = glob.glob('/home/pi/RPi-Ardunio/Robot/RPiCode/*.jpg')
        track_image = max(list_files, key=os.path.getctime)
    #     print ("track image file: ", track_image)
    #     logging.info('track image file: {a}'.format (a=track_image))
        img = cv2.imread(track_image,cv2.IMREAD_GRAYSCALE)

        detector = apriltag.Detector()

        result = detector.detect(img)
        
        if result == []:
            print ("Empty arrary - no targets found")
            logging.info('Empty array')
            # at this point go to target search routine
        else:           
        
            xcpx = -1 # used to check if no robot target detected
            for i in range(len(result)):
                # look for targets on robot(s) as of this writing apriltag #499
                if result[i].tag_id != 499:
                    # call def to extract center x,y pixels
                    xcpx, ycpx = extract_center(result, i)
                    #print('\n', "tag id= ", result[i].tag_id, "  target center: ", xcpx, "  ", ycpx)
                    ytlpx, yllpx = extract_corner(result, i)
                    #print("left corners: ", ytlpx, "  ", yllpx)
                    obj_hgt = int(yllpx - ytlpx)
                    #print("robot target object height: ", obj_hgt)
                    
                                
                    # call def to calculate range to robot (def calc_range)
                    r_range = calc_range(obj_hgt, 86)
                    #print("Robot range: ", r_range)
                    logging.info('Robot target object height and range: {a}, {b}'.format (a=obj_hgt, b=r_range))
                    ratio_r = (xcpx - img_h)/r_range
                    #print('\n', 'robot ratio: ', ratio_r)
                    
                    xdelta = xcpx - img_cx
                    # calculate the estimated step size to center image on tag
                    stepsz = 637 * math.asin(0.000703*(xdelta*r_range)/r_range)
                    if (abs(xdelta) < 10):
                        lock = 1
                        print("Lock")
                    else:
                        cur_az = cur_az + stepsz
                        print('Step size: ', stepsz, ' Tag center: ', xcpx, ' Current pwm: ', cur_az, ' Current angle: ', (cur_az-500)/11.1)
                        logging.info('Step size, tag center, pwm and az: {a}, {b}, {c}, {d}'.format (a=stepsz,b=xcpx,c=cur_az,d=(cur_az-500)/11.1))
                        pwm.set_servo_pulsewidth(servo, cur_az)
                   
        
                    
                
                #rr_list = []
                # cycle through fiducial targets to calculate ratio px offset to range,
                # and 'ratio-of-ratio' for each to build r-of-r list
#                 for i in range(len(targets)):
#                     ratio_i = float(targets[i][7] - 640)/float(targets[i][3])
#                     
#                     r_of_r = abs(1 - (ratio_i/ratio_r))
#                     print('\n', 'i= ', i, '  tag id= ', targets[i][0], '  ratio_i= ', ratio_i)
#                     rr_list.append(r_of_r)
#                     print('\n', 'rr_list: ', rr_list)
#                     logging.info('rr_list: {a}'.format (a=rr_list))
#                 # find minimum ratio of ratio, meaning the robot is closest in azimuth to
#                 # that fiducial target
#                 minpos = rr_list.index(min(rr_list))
#                 print('\n', 'minpos: ', minpos, '  r of r: ', rr_list[minpos])
#                 # calculate robot x,y in arena coords
#                 deg = targets[minpos][10]
#                 rad = round(math.radians(deg),4)
#                 robx = int(2000 + (r_range * math.sin(rad))) # x in mm in arena coords
#                 roby = int(r_range * math.cos(rad)) # y in mm in arena coords
#                 print('\n', 'deg, rad, robx, roby: ', deg,'  ', rad,'  ', robx,'  ', roby)
#                 logging.info('deg, rad, robx, roby: {a}, {b}, {c}, {d} '.format (a=deg,b=rad,c=robx,d=roby))           

if xcpx <0:
        print ("No targets detected")
        logging.info('No targets detected')

"""
= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
   Transmit Robot(s) Position to Controller
= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
"""
camera.stop_preview()
sys.exit()