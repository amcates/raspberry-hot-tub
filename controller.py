#!/usr/bin/python
#import RPi.GPIO as GPIO
import threading
import time
import datetime
import os

### code for accepting input from the push button to activate the filtration pump (aka jets)
#
#GPIO.setmode(GPIO.BCM)
#
#button_pin = "YOUR_PIN_GOES_HERE"
#GPIO.setup(button_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#
#def isPressed(button_pin):
#    now = time.time()
#    if GPIO.input(button_pin) == False:
#        time.sleep(DEBOUNCE)
#        # wait for button release
#        while not GPIO.input(button_pin):
#            pass
#    	return True
#    return False
#
#def buttonPress(button_pin):
#    if isPressed(button_pin):
#	start_filtration(3600)
#
#def buttonRelease(channel):
#    if not isPressed(button_pin):
#        stop_filtration()
#
#GPIO.add_event_detect(button_pin,GPIO.RISING,callback=buttonPress)
#GPIO.add_event_detect(button_pin,GPIO.FALLING,callback=buttonRelease)

### code for reading from temperature sensor (#TODO we will use 2 sensors so this will need to be modified)

def read(ds18b20):
    location = ds18b20 # '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
    tfile = open(location)
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    celsius = temperature / 1000
    farenheit = (celsius * 1.8) + 32
    return farenheit

### code for running the pumps and heater

def start_filtration():
    global current_state

    if current_state == 'filtration_on':
        print("Filtration already on")
    else:
        current_state = 'filtration_on'

        print("Turning filtration pump on")
        # insert code to turn filtration on

def stop_filtration():
    global current_state

    current_state = None
    print("Turning filtration pump off")
    # insert code to turn filtration off

def cycle_filtration(duration):
    start_filtration()
    time.sleep(duration) 
    stop_filtration()

def start_circulation_pump():
    print("Turning circulation pump on")
    # insert code to turn circulation on

def stop_circulation_pump():
    print("Turning circulation pump off")
    # insert code to turn circulation off

def start_heater():
    global current_state

    print("Turning on heater")
    # replace this with code to turn heater on

def stop_heater():
    print("Turning off heater")
    # replace this with code to turn heater off

### logic to determine how the system responds to different temperatures

def determine_action(current_temp=104):
    global current_state, threaded_timer

    print("Current temp is " + str(current_temp))
    current_state = 'heating'
    pause_between_checks = TEST_SLEEP_FOR if TEST_MODE else PAUSE_BETWEEN_CHECKS_FOR

    if current_temp >= 104:
        print("Temperature is good, nothing to do")
        stop_all()
        print("Waiting " + str(pause_between_checks) + " seconds before we check again")
        time.sleep(pause_between_checks) # temp is good, we should wait a little while before we check again
    elif current_temp < 96:
        delay = TEST_SLEEP_FOR if TEST_MODE else LONG_RUN
        print("Temperature is less than 96, running for " + str(delay) + " seconds")
    elif 96 <= current_temp <= 99:
        delay = TEST_SLEEP_FOR if TEST_MODE else MED_RUN
        print("Temperature is between 98 and 100, running for " + str(delay) + " seconds")
    elif 100 <= current_temp <= 103:
        delay = TEST_SLEEP_FOR if TEST_MODE else SHORT_RUN
        print("Temperature is between 100 and 103, running for " + str(delay) + " seconds")

    if current_state == 'heating':
	start_circulation_pump()
        start_heater()
        if TEST_MODE: 
	    time.sleep(delay)
            stop_all()
	else:
            threaded_timer = delayed_stop(stop_all, delay)

def delayed_stop(func, timeout):
   def func_wrapper(): func()

   t = threading.Timer(timeout, func_wrapper, ())
   t.start()

   return t 

def stop_all():
    global threaded_timer

    if threaded_timer: threaded_timer.cancel() 

    stop_heater()
    stop_filtration()
    stop_circulation_pump()

    reset_state()

def reset_state():
    global current_state
    print("Resetting current_state to None")
    current_state = None

def kill():
    stop_all()
    quit()

if __name__ == '__main__':
    try:
	## NOTE ALL TIMES ARE IN SECONDS

	# usage: TEST_MODE=true python controller.py
        TEST_MODE = True if os.environ.get('TEST_MODE', 'false') == 'true' else False
        TEST_SLEEP_FOR = 3

	# how long do we wait between checks when the temperature is 104+
	PAUSE_BETWEEN_CHECKS_FOR = 20

	# how long to cycle filtration before we check the temperature
        CYCLE_FILTRATION_FOR = 20

	# debounce time for push buttons
        DEBOUNCE = 0.2

	# how long the heater will run under certain conditions, see def determine_action
	LONG_RUN  = 5400
        MED_RUN   = 3600
        SHORT_RUN = 1800

	# current state of the system, [None, filtration_on, heating]
        current_state = None

	# threaded timer used in def delayed_stop
        threaded_timer = None

	### make sure all systems are off when first starting up ###
        print("################### System Startup #####################")
        stop_all()
        print("\n")
	
        if TEST_MODE == True:
            print("############### Starting TEST procedure ###############")

            for current_temp in [104, 102, 97, 95]:
                print("Starting procedure for " + str(current_temp))
                print("--------------------------")
		cycle_filtration(TEST_SLEEP_FOR)
                determine_action(current_temp)
                print("\n")

            print("################### End TEST ########################")
        else:
            print("############ Starting to monitor temperature ############")
            while True:
		if current_state == None:
                    #Heat Mode (we want 104)
		    cycle_filtration(CYCLE_FILTRATION_FOR)
 
                    if read("temperature.txt") != None:
                        current_temp = read("temperature.txt")
                        determine_action(current_temp)
	    	    else:
    		        stop_all()

    except KeyboardInterrupt:
        kill()


### code for 4 channel relay
#
#GPIO.setmode(GPIO.BCM)
#
## init list with pin numbers
#
#pinList = [2, 3, 4, 17]
#
## loop through pins and set mode and state to 'high'
#
#for i in pinList:
#    GPIO.setup(i, GPIO.OUT)
#    GPIO.output(i, GPIO.HIGH)
#
## time to sleep between operations in the main loop
#
#SleepTimeL = 2
#
## main loop
#
#try:
#  GPIO.output(2, GPIO.LOW)
#  print "ONE"
#  time.sleep(SleepTimeL);
#  GPIO.output(3, GPIO.LOW)
#  print "TWO"
#  time.sleep(SleepTimeL);
#  GPIO.output(4, GPIO.LOW)
#  print "THREE"
#  time.sleep(SleepTimeL);
#  GPIO.output(17, GPIO.LOW)
#  print "FOUR"
#  time.sleep(SleepTimeL);
#  GPIO.cleanup()
#  print "Good bye!"
#
## End program cleanly with keyboard
#except KeyboardInterrupt:
#  print "  Quit"
#
#  # Reset GPIO settings
#  GPIO.cleanup()
#
#
## find more information on this script at
## http://youtu.be/WpM1aq4B8-A
