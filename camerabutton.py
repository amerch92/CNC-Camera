from datetime import datetime
import picamera
import time
from subprocess import call
import os

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP) #setup switch

GPIO.setup(17, GPIO.OUT) # Blue
GPIO.setup(27, GPIO.OUT) # green
GPIO.setup(22, GPIO.OUT) # red

pc=picamera.PiCamera()


global folderlocation
folderol = "/home/pi/Desktop/"
folderlocation = ""

global status1
running = True

status1 = False
  
i = 1

while True:
    try:
        if GPIO.input(14) == 1:
            
            GPIO.output(22, GPIO.HIGH)
            
            if status1 == False:
                timestamp = datetime.now()
                folderlocation = str(timestamp)
                os.mkdir(folderol + folderlocation)
                status1 = True
                
            print('Active' + str(i))
            if status1 == True:    
                pc.resolution = (1920, 1080)
                pc.capture(folderol + folderlocation + "/" + str(i) + "_pic.jpg")
                i = i + 1
                GPIO.output(27, GPIO.HIGH)
                time.sleep(2)
                GPIO.output(27, GPIO.LOW)
            else:
                i = 1
            time.sleep(1)
        else:
            print('Not Pressed')
            time.sleep(2)
            status1 = False
            GPIO.output(22, GPIO.LOW)
            
    except KeyboardInterrupt:
        pc.stop_preview()
        running = False
