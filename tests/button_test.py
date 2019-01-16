#!/usr/bin/python3
import RPi.GPIO as GPIO
import time


### code for accepting input from the push button to activate the filtration pump (aka jets)
#
GPIO.setmode(GPIO.BCM)
#
button_pin = 26
GPIO.setup(button_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#
def isPressed(button_pin):
    now = time.time()
    if GPIO.input(button_pin) == False:
        time.sleep(DEBOUNCE)
        # wait for button release
        while not GPIO.input(button_pin):
            pass
       	return True
    return False

def buttonPress(button_pin):
    if isPressed(button_pin):
       start_filtration(3600)

def buttonRelease(channel):
    if not isPressed(button_pin):
        stop_filtration()

GPIO.add_event_detect(button_pin,GPIO.RISING,callback=buttonPress)
GPIO.add_event_detect(button_pin,GPIO.FALLING,callback=buttonRelease)
