import sys
import RPi.GPIO as GPIO
import os
from time import sleep
import Adafruit_DHT
import urllib2


DEBUG = 1
# Setup the pins we are connect to
DHTpin = 23
myDelay = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(RCpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)



def getSensorData():
    RHW, TW = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin)

    #Convert from Celius to Farenheit
    TWF = 9/5*TW+32

    # return dict
    return (str(RHW), str(TW),str(TWF))

def main():

    print 'starting...'

    while True:
        try:
            RHW, TW, TWF = getSensorData()
            print(TW + " " + TWF+ " " + RHW )


            sleep(int(myDelay))
        except:
            print 'exiting.'
            break

if __name__ == '__main__':
    main()
