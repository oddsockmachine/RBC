from picamera import PiCamera
from time import sleep

camera = PiCamera()
sleep(3)
print("starting")
camera.capture('./image.jpg')
