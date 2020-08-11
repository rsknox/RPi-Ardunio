import P3picam
import picamera
from datetime import datetime
from subprocess import call
from time import sleep
from cookieClient3 import backup
from cookieAnalog2 import getTemp
import time

motionState = False
#picPath = "/home/pi/Desktop/cookie/images/"
#picPath = "/home/pi/Desktop/"
picPath = "/home/pi/Git/RPi-Ardunio/"
sleepTime = 3
triggerTemp = 20

def captureImage(currentTime, picPath):
    # Generate the picture's name
    now = time.time()
    #strip off msb part, leaving today's seconds
    ny = int(now/100000)
    ny = now - (ny*100000)
    now = round(ny,3) # time since epoch rounded to msec
    now = str(now)
    #file_name = "/home/pi/Git/RPi-Ardunio/" + name + datetime.datetime.now().strftime("%Y%m%d-%H%M%S.jpg")
    picName = "Camera_Zx_" + now + '.jpg'
    #picName = currentTime.strftime("%Y.%m.%d-%H%M%S") + '.jpg'
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        camera.capture(picPath + picName)
    print("We have taken a picture.")
    return picName

def getTime():
    # Fetch the current time
    currentTime = datetime.now()
    return currentTime

def timeStamp(currentTime, picPath, picName):
    # Variable for file path
    filepath = picPath + picName
    # Create message to stamp on picture
    message = currentTime.strftime("%Y.%m.%d - %H:%M:%S")
    # Create command to execute
    timestampCommand = "/usr/bin/convert " + filepath + " -pointsize 36 \
    -fill red -annotate +700+650 '" + message + "' " + filepath
    # Execute the command
    call([timestampCommand], shell=True)
    print("We have timestamped our picture.")

def tempMonitor():
    print("About to take a reading.")
    temp = float(getTemp())
    print("Out temp is: " + str(temp))
    if temp > float(triggerTemp):
        message = "LED_ON"
        print("Transmitting data.")
        response = transmit(message)
        print(response)

while True:
    currentTime = getTime()
    picName = captureImage(currentTime, picPath)
    print("Took a picture")
    completePath = picPath + picName
    print(completePath)
    backup(completePath)
    print("Everything should be backed up now.")
    break
    #motionState = P3picam.motion()
    #tempMonitor()
    #sleep(sleepTime)
    #print(motionState)
    #if motionState:
    #    currentTime = getTime()
    #    picName = captureImage(currentTime, picPath)
    #    timeStamp(currentTime, picPath, picName)
        
