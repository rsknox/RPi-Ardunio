import time
import picamera
with picamera.PiCamera() as camera:
    camera.start_preview()
    try:
        for i, filename in enumerate(camera.capture_continuous('K{counter:02d}.jpg')):
            print(filename)
            time.sleep(.1)
            if i == 10:
                break
    finally:
        camera.stop_preview()