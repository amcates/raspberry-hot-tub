#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
## code for 4 channel relay


# init list with pin numbers

pinList = [23,24,25]

# loop through pins and set mode and state to 'high'

GPIO.setmode(GPIO.BCM)
for i in pinList:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.LOW)

# time to sleep between operations in the main loop

SleepTimeL = 4

# main loop

try:
    for i in pinList:
        print(str(i))
        GPIO.output(i, GPIO.HIGH)
        time.sleep(SleepTimeL)
        GPIO.output(i, GPIO.LOW)
    GPIO.cleanup()


# End program cleanly with keyboard
except KeyboardInterrupt:
  print("Quit")

  # Reset GPIO settings
  GPIO.cleanup()


# find more information on this script at
# http://youtu.be/WpM1aq4B8-A
