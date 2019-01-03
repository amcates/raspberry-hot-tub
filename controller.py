#!/usr/bin/python
#import RPi.GPIO as GPIO
import time
import os


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
 
def run_filtration(sec=20):
    print("Running filtration pump for " + str(sec) + " seconds")
    time.sleep(sec)
    print("Turning filtration pump off")

def start_circulation_pump(): 
    print("Turning circulation pump on")
    time.sleep(5)

def stop_circulation_pump():
    print("Turning circulation pump off")

def run_heater(sec=0):
    start_circulation_pump() 
    print("Running heater for " + str(sec) + " seconds")
    sec = 5 # temporary for testing purposes
    time.sleep(sec)
    print("Turning off heater")
    stop_circulation_pump()

def determine_action(current_temp=104):
    print("Current temp is " + str(current_temp))

    if current_temp >= 104:
	print("Temperature is good, sleeping for 1.5 hrs")
	time.sleep(5)
	#time.sleep(5400)
    elif current_temp < 96:
	print("Temperature is less than 96, running for 1.5 hrs")
        run_heater(5400)
    elif 96 <= current_temp <= 99:
	print("Temperature is between 98 and 100, running for 1 hr")
        run_heater(3600)
    elif 100 <= current_temp <= 103:
	print("Temperature is between 100 and 103, running for 30 min")
        run_heater(1800)

    time.sleep(10)

def kill():
    quit()
 
if __name__ == '__main__':
    try:
	while True:

	    #Heat Mode (we want 104)

	    run_filtration(2)

	    if read("temperature.txt") != None:
		current_temp = read("temperature.txt")
		determine_action(current_temp)

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
