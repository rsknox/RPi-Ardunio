from picamera import PiCamera
from time import sleep
import datetime
import sys
import signal
import threading
import time
import schedule
import logging
logging.basicConfig(filename='logCamera.log', level=logging.INFO, format='%(asctime)s %(message)s')

def signal_handler(sig, frame):
    print('ctrl-c detected')
    logging.info('ctrl-c detected')
    sys.exit(0)

def i_capture(name):
    file_name = "/home/pi/RPi-Ardunio/" + name + datetime.datetime.now().strftime("%Y%m%d-%H%M%S.jpg")
#    file_name = "/home/pi/RPi-Ardunio/apriltags" + file_name
#camera.capture('/home/pi/RPi-Ardunio/apriltags%s.jpg' %j)
    camera.capture(file_name)
    print('\n', file_name)
    logging.info('File name: {a}'.format (a=file_name))

signal.signal(signal.SIGINT, signal_handler)
logging.info('Start')
camera = PiCamera()
camera.resolution = (1280, 1024)
#camera.start_preview()
camera.start_preview(fullscreen=False, window=(100,100,512,384))

schedule.every(1.0).seconds.do(i_capture,'C_vnc_25Jun')

sleep(2)  # give camera time to stablize
now = int(round(time.time() * 1000))
ter = now + 10000
while now < ter:
    schedule.run_pending()
    now = int(round(time.time() * 1000))
#    print('\n', 'now: ', now)
    #logging.info('now: {a}'.format (a=now))
    

# file_name = datetime.datetime.now().strftime("%Y%m%d-%H%M%S.jpg")
# print (file_name)
# file_name = "/home/pi/RPi-Ardunio/apriltags" + file_name
# print('\n', file_name)
# #camera.capture('/home/pi/RPi-Ardunio/apriltags%s.jpg' %j)
# camera.capture(file_name)

# msec = int(round(time.time() * 1000))
# print('\n', 'time now: ', msec)
# next_i = msec + 1000
# print('\n', 'next image: ', next_i)
# for i in range(10):
#     sleep(.5)
#     now = int(round(time.time() * 1000))
#     if now >= next_i:
#         i_capture()
#         print('\n', 'now = ', now)
#         next_i = now +1000
        

# for i in range(5):
#     j = i+2000
#     sleep(1)
#     file_name = datetime.now().strtime("/home/pi/RPi-Ardunio/apriltags%Y%m%d-%H%M%S.jpg")
# #    camera.capture('/home/pi/RPi-Ardunio/apriltags%s.jpg' %j)
#     camera.capture(filename)

# camera.start_recording('video_a.h264')
# sleep(6)
# camera.stop_recording()
camera.stop_preview()
sys.exit()
