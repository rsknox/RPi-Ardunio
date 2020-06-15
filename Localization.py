# 7 Jun 2020; 1350
# Localization - routine to capture an image every second from a camera
# at a fixed location, detect the apriltag of each robot in the arena,
# estimate each robots position (x,y in arena coordinates) and transmit
# to the controller

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



def signal_handler(sig, frame):
    print('ctrl-c detected')
    logging.info('ctrl-c detected')
    sys.exit(0)

def i_capture(name):
    file_name = "/home/pi/RPi-Ardunio/" + name + datetime.datetime.now().strftime("%Y%m%d-%H%M%S.jpg")
    camera.capture(file_name)
    print('\n', file_name)
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
    focal_len = 3.6  # camera focal length in mm
    image_hgt = 1024  # image height in px
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

logging.basicConfig(filename='log_Localization.log', level=logging.INFO, format='%(asctime)s %(message)s')
signal.signal(signal.SIGINT, signal_handler)
schedule.every(1.0).seconds.do(i_capture,'track_i')

# insert parameters and constants

camera = PiCamera()
camera.resolution = (1280, 1024)
# CSV file parameters
gndTfilename = "gndTrth.csv"
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

l=0 # will loop and capture calibration images until tag 0 is in center
    # asks for input at end of loop enter either '0' loop again or non-zero
    # to continue with the program
while l==0:
    
    i_capture('calibration')
    list_files = glob.glob('/home/pi/RPi-Ardunio/*.jpg')
    cal_image = max(list_files, key=os.path.getctime)
    print ("calibration image file: ", cal_image)
    logging.info('Calibration image file: {a}'.format (a=cal_image))
    img = cv2.imread(cal_image,cv2.IMREAD_GRAYSCALE)
    #stub code for test
    # photo = 'apriltags1004.jpg'
    # img = cv2.imread(photo,cv2.IMREAD_GRAYSCALE)

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
                # scroll through the ground truth targets looking for a tag match
                for k in range(len(targets)):
                    #print('\n', 'k= ', k, ' targets tag= ',targets[k][0],' detected tag= ',result[i].tag_id, ' xcpx= ', xcpx)
                    if int(targets[k][0]) == int(result[i].tag_id):
                        
                        # if gndT tag id matches detected tag id, write px coord to the list                 
                        targets[k][7] = int(xcpx)
                        targets[k][8] = int(ycpx)
                        r_hgt = float(targets[k][6])
                
                logging.info('Detected tags added to list: {a}'.format (a=targets))
                ytlpx, yllpx = extract_corner(result, i)
                print("left corners: ", ytlpx, "  ", yllpx)
                obj_hgt = int(yllpx - ytlpx)
                print("robot target object height: ", obj_hgt)
                logging.info('Robot target object height: {a}'.format (a=obj_hgt))
                            
                # call def to calculate range to robot (def calc_range)
                r_range = calc_range(obj_hgt, r_hgt)
                print("Robot range: ", r_range)
                # call def to estimate robot azimuth angle (def calc_az_angle)
                # call def to calculate robot x,y location in arena coordinates (def calc_rposn)
            else:
                pass

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
    #camera.start_preview(fullscreen=False, window=(100,100,512,384))

    #schedule.every(1.0).seconds.do(i_capture,'track_i')
    # following code is to limit the test cycle to x (nominal 10) sec
    now = int(round(time.time() * 1000))
    ter = now + 10000
    while now < ter:
        schedule.run_pending()
        now = int(round(time.time() * 1000))
        """
        = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
        Detect Robot(s) Targets
        = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
        """
        list_files = glob.glob('/home/pi/RPi-Ardunio/*.jpg')
        track_image = max(list_files, key=os.path.getctime)
        print ("track image file: ", track_image)
        logging.info('track image file: {a}'.format (a=track_image))
        img = cv2.imread(cal_image,cv2.IMREAD_GRAYSCALE)

        detector = apriltag.Detector()

        result = detector.detect(img)
        xcpx = -1 # used to check if no robot target detected
        for i in range(len(result)):
            # look for targets on robot(s) as of this writing apriltag #499
            if result[i].tag_id == 499:
                # call def to extract center x,y pixels
                xcpx, ycpx = extract_center(result, i)
                print('\n', "tag id= ", result[i].tag_id, "  target center: ", xcpx, "  ", ycpx)
                ytlpx, yllpx = extract_corner(result, i)
                print("left corners: ", ytlpx, "  ", yllpx)
                obj_hgt = int(yllpx - ytlpx)
                print("robot target object height: ", obj_hgt)
                logging.info('Robot target object height: {a}'.format (a=obj_hgt))
                            
                # call def to calculate range to robot (def calc_range)
                r_range = calc_range(obj_hgt, 51)
                print("Robot range: ", r_range)
                # call def to estimate robot azimuth angle (def calc_az_angle)
                # call def to calculate robot x,y location in arena coordinates (def calc_rposn)

        if xcpx <0:
            print ("No targets detected")
            logging.info('No targets detected')


"""
= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
   Calculate Robot(s) Position
= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
"""


"""
= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
   Transmit Robot(s) Position to Controller
= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
"""
camera.stop_preview()
sys.exit()