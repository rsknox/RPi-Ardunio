# Camera Test - test operation of cameras on RPi Zero
# first execute cmd 'raspistill -o imgage.jpg' to test the camera to Zero connection

from picamera import PiCamera
from time import sleep
import datetime
#import cv2
import math
import time
import glob
import os
import sys
import signal
import logging

def signal_handler(sig, frame):
    print('ctrl-c detected')
    logging.info('ctrl-c detected')
    sys.exit(0)

def i_capture(name):
    now = time.time()
    #strip off msb part, leaving today's seconds
    ny = int(now/100000)
    ny = now - (ny*100000)
    now = round(ny,3) # time since epoch rounded to msec
    now = str(now)
    #file_name = "/home/pi/Git/RPi-Ardunio/" + name + datetime.datetime.now().strftime("%Y%m%d-%H%M%S.jpg")
    file_name = "/home/pi/Git/RPi-Ardunio/" + name + '_'+ now + '.jpg'
    camera.capture(file_name)
    print('\n', file_name)
    logging.info('File name: {a}'.format (a=file_name))
    
logging.basicConfig(filename='CameraTest.log', level=logging.INFO, format='%(asctime)s %(message)s')
signal.signal(signal.SIGINT, signal_handler)


camera = PiCamera()
camera.resolution = (1280, 1024)

logging.info('Start camera')

camera.start_preview(fullscreen=False, window=(700,100,512,384))
sleep(2)  # give camera time to stablize

for i in range(10):
    i_capture('Camera_Zx')
    
#     list_files = glob.glob('/home/pi/Git/RPi-Ardunio/*.jpg')
#     cal_image = max(list_files, key=os.path.getctime)
#     print ("CameraZx image", cal_image)
#     logging.info('CameraZx image file: {a}'.format (a=cal_image))
sleep(2) # ensure final images written to disk before exit               
camera.stop_preview()
sys.exit()