#!/usr/bin/python3
import RPi.GPIO as GPIO
import threading
import socket
import time
import datetime
import os
import json
import logging
from RPLCD.i2c import CharLCD

from button import *

### code for reading from temperature sensor (#TODO we will use 2 sensors so this will need to be modified)

def read(ds18b20):
    location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'

    try: 
        tfile = open(location)
        text = tfile.read()
        tfile.close()
        secondline = text.split("\n")[1]
        temperaturedata = secondline.split(" ")[9]
        temperature = float(temperaturedata[2:])
        celsius = temperature / 1000
        farenheit = (celsius * 1.8) + 32
    except FileNotFoundError:
        farenheit = 500.0

    return round(farenheit, 2)

### code for running the pumps and heater

def start_filtration():
    # make sure the other systems are off first
    if get_state() == 'start_heater':
        stop_heating_cycle()

    if get_state() == 'start_filtration':
        log("Filtration already on")
    else:
        relay_on(RELAY_1)
        change_state('start_filtration')

        log("Turning filtration pump on")
        # insert code to turn filtration on

    return "Filtration pump turned on"

def stop_filtration():
    relay_off(RELAY_1)
    log("Turning filtration pump off")
    # insert code to turn filtration off
    return "Filtration pump turned off"

def cycle_filtration(duration):
    start_filtration()
    time.sleep(duration) 
    stop_filtration()

def start_circulation_pump():
    relay_on(RELAY_2)
    log("Turning circulation pump on")
    # insert code to turn circulation on
    return "Circulation pump turned on"

def stop_circulation_pump():
    relay_off(RELAY_2)
    log("Turning circulation pump off")
    # insert code to turn circulation off
    return "Circulation pump turned off"

def start_heater():
    relay_on(RELAY_3)
    change_state('start_heater')
    log("Turning on heater")
    # replace this with code to turn heater on
    return "Heater turned on"

def stop_heater():
    relay_off(RELAY_3)
    log("Turning off heater")
    # replace this with code to turn heater off
    return "Heater turned off"

### logic to determine how the system responds to different temperatures

def determine_action():
    global threaded_timer
    
    current_temp = get_temp()

    if get_state() == 'start_filtration':
        stop_filtration()

    log("Current temp is " + str(current_temp))
    change_state('start_heater') #TODO Does this need to be here, in order for the below code to work it does

    if current_temp >= 104:
        log("Temperature is good, nothing to do")
        system_reset()
        change_state('monitor_only')
        log("Waiting " + str(PAUSE_BETWEEN_CHECKS_FOR) + " seconds before we check again")
        threaded_timer = delayed_stop(system_reset, PAUSE_BETWEEN_CHECKS_FOR) # temp is good, we should wait a little while before we check again
    elif current_temp < 96:
        delay = LONG_RUN
        log("Temperature is less than 96, running for " + str(delay) + " seconds")
    elif 96 <= current_temp <= 99:
        delay = MED_RUN
        log("Temperature is between 98 and 100, running for " + str(delay) + " seconds")
    elif 100 <= current_temp <= 103:
        delay = SHORT_RUN
        log("Temperature is between 100 and 103, running for " + str(delay) + " seconds")

    if get_state() == 'start_heater':
        start_circulation_pump()
        start_heater()
        threaded_timer = delayed_stop(system_reset, delay)

def delayed_stop(func, timeout):
    def func_wrapper(): func()

    t = threading.Timer(timeout, func_wrapper, ())
    t.start()

    return t 

def stop_heating_cycle():
    global threaded_timer

    if threaded_timer: threaded_timer.cancel() 

    stop_heater()
    stop_circulation_pump()

def system_reset():
    global threaded_timer

    if threaded_timer: threaded_timer.cancel() 

    stop_heater()
    stop_filtration()
    stop_circulation_pump()

    reset_state()

    return "All systems stopped and state reset"

def reset_state():
    change_state(None)
    log("Resetting current_state to None")
    return "System state set to None"

def system_off():
    system_reset()
    change_state('system_off')
    log("Turning the system off")
    return "System turned off"

def get_temp():
    current_temp = None

    if read("28-021892458db6") != None:
        current_temp = read("28-021892458db6")

    return current_temp

def json_value(attr, value):
    x = {attr: value}
    return json.dumps(x)

def change_state(new_state):
    global current_state
    log("State changed from " + str(current_state) + " to " + str(new_state))
    current_state = new_state

def get_state():
    return current_state

### listening server handler
def handle(clientsocket, address):
    commands = ['start_filtration', 'start_heater', 'system_off', 'get_temp', 'get_state']
    command_dict = {'start_filtration' : start_filtration,
                    'start_heater'     : system_reset,
                    'system_off'       : system_off,
                    'get_temp'         : get_temp,
                    'get_state'        : get_state,
                }
    try:
        while 1:
            buf = clientsocket.recv(MAX_LENGTH)
            if buf == '': return #client terminated connection
            
            command = buf.decode('utf-8')
            if command in commands:
                resp = command_dict[command]()
                valid = "Connection: " + str(address[0]) + " Command Received: " + str(command) + " Response: " + str(resp)
                if str(address[0]) != '127.0.0.1':
                    log(valid)
                clientsocket.send(str(resp).encode('utf-8'))
            else:
                invalid = "Connection: " + str(address[0]) + " Invalid Command: " + str(command)
                if str(address[0]) != '127.0.0.1':
                    log(invalid)
                clientsocket.send(invalid.encode('utf-8'))
                
            break
    finally:
        clientsocket.close()


### handle button push

def navigation_button():
    while 1:
        if exit_now:
            break

        if FILTRATION_BUTTON.is_pressed():
            if get_state() == 'start_filtration':
                system_reset()
            else:
                start_filtration()

def update_lcd():
    global last_lcd_temp, last_lcd_state

    start_time = time.process_time()
    display_version = True

    while 1:
        if exit_now:
            break

        temp_readout = str(get_temp()) + chr(223) + "F"

        # this case handles if the sensor isn't providing data or the sensor file doesn't exist, it basically makes the system thinks it's too hot (prevent heating)
        if temp_readout == '500.0' + chr(223) + 'F': 
            temp_readout = 'Sensor Failed'

        state = str(get_state())
        state_readout = 'Unknown'
        current_time = time.process_time()
        elapsed_time = current_time - start_time

        if state in ['None', 'monitor_only']:
            state_readout = 'Monitoring Temp'
        elif state == 'start_filtration':
            state_readout = 'Jets On'
        elif state == 'start_heater':
            state_readout = 'Heater On'
        elif state == 'system_off':
            state_readout = 'System Off'

        if last_lcd_temp != temp_readout or last_lcd_state != state_readout:
            last_lcd_temp = temp_readout
            last_lcd_state = state_readout
            start_time = time.process_time()

            lcd_write(temp_readout, state_readout)
        elif elapsed_time > 30 and display_version == True:
            lcd_write(SYS_VERSION, "   " + datetime.date.today().strftime('%m/%d/%Y'))
            display_version = False
        elif elapsed_time > 40:
            start_time = time.process_time()
            display_version = True
            last_lcd_temp = None

def relay_on(pin):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.2)

def relay_off(pin):
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.2)

def lcd_write(line_1, line_2):
        LCD.cursor_pos = (0,0)
        LCD.write_string(line_1.ljust(16))
        LCD.cursor_pos = (1,0)
        LCD.write_string(line_2.ljust(16))

def log(message):
    global last_logged

    # only log if the message has changed, this should save some disk space and keep the log from growing too fast
    if not message == str(last_logged):
        logging.info(message)
        last_logged = message

### exit application
def kill():
    global exit_now
    exit_now = True

    system_reset()
    change_state('system_off')
    lcd_write("Good Bye!", "System Off")
    logging.error("System Shutdown")
    GPIO.cleanup()
    quit()

if __name__ == '__main__':
    try:
        ## NOTE ALL TIMES ARE IN SECONDS

        logging.basicConfig(filename='./logs/controller.log', format='%(asctime)s: %(levelname)s: %(message)s', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')
        last_logged = None
        
        SYS_VERSION = "Hot Springs v1.0"

        # max and min temps
        MAX_TEMP=104.0
        MIN_TEMP=102.0

        # how long do we wait between checks when the temperature is 104+
        PAUSE_BETWEEN_CHECKS_FOR = 5400

        # how long to cycle filtration before we check the temperature
        CYCLE_FILTRATION_FOR = 5

        # debounce time for push buttons
        DEBOUNCE = 0.5

        # Button used to turn filtration on/off
        FILTRATION_BUTTON_GPIO = 26
        FILTRATION_BUTTON = Button(FILTRATION_BUTTON_GPIO, debounce=DEBOUNCE)

        # how long the heater will run under certain conditions, see def determine_action
        LONG_RUN  = 7200
        MED_RUN   = 5400
        SHORT_RUN = 3600

        # configuration for server listening for commands
        MAX_LENGTH = 4096
        PORT = 10000
        HOST = '127.0.0.1'
        TIMEOUT = 2
        LISTEN = 10

        # LCD 16x2 i2c
        LCD = CharLCD('PCF8574', 0x27)
        last_lcd_state = ''
        last_lcd_temp = None

        # 4 channel relay
        GPIO.setmode(GPIO.BCM)
        # relay 1 = 23, filtration pump
        # relay 2 = 24, circulation pump
        # relay 3 = 25, heater
        # relay 4 = 12, currently not used, maybe for a dehumidifier
        RELAY_1 = 23 # currently allocated to filtration pump
        RELAY_2 = 24 # currently allocated to circulation pump
        RELAY_3 = 25 # currently allocated to heater
        RELAY_4 = 12 # not currently used, issue with Raspberry PI and voltage
        
        pinList = [RELAY_1, RELAY_2, RELAY_3] # RELAY_4 left out on purpose
        
        for i in pinList:
            GPIO.setup(i, GPIO.OUT)

        # exit flag, used to make threads exit cleanly
        exit_now = False

        # current state of the system, [None, start_filtration, start_heater, system_off, monitor_only]
        current_state = None

        # threaded timer used in def delayed_stop
        threaded_timer = None

        ### make sure all systems are off when first starting up ###
        log("################### System Startup #####################")
        system_reset()

        log("Starting up listening server")
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((HOST, PORT))
        serversocket.settimeout(TIMEOUT)
        serversocket.listen(LISTEN)

        log("######### Starting to monitor for commands and  temperature ########")
        
        navigation_button_thread = threading.Thread(target=navigation_button)
        navigation_button_thread.daemon = True
        navigation_button_thread.start()
        
        lcd_thread = threading.Thread(target=update_lcd)
        lcd_thread.daemon = True
        lcd_thread.start()

        while 1:
           
            # make it easy to stop the application via file
            if os.path.isfile('./shutdown.txt'):
                os.remove('./shutdown.txt')
                kill()

            #accept connections from outside
            try:
                (clientsocket, address) = serversocket.accept()

                client_thread = threading.Thread(target=handle, args=(clientsocket,address))
                client_thread.daemon = True
                client_thread.start()
            #TODO this doesn't seem to be working
            except socket.timeout:
                if get_state() == None:
                    #Heat Mode (we want 104)
                    cycle_filtration(CYCLE_FILTRATION_FOR)
 
                    if get_temp():
                        determine_action()
                    else:
                        system_reset()
                elif get_state() == 'monitor_only' or get_state() == 'start_heater':
                    # if the temp drops below lower threshhold turn on the heater early, if it gets to upper threshhold early turn the heater off 
                    temp = get_temp()
                    if temp < MIN_TEMP:
                        log("Temperature (" + str(temp) + ") is below desired temperature")
                        if get_state() != 'start_heater':
                            system_reset()
                    elif temp > MAX_TEMP:
                        log("Temperature (" + str(temp) + ") is above desired temperature")
                        if get_state() != 'monitor_only':
                            system_reset()
                            change_state('monitor_only')
                            threaded_timer = delayed_stop(system_reset, PAUSE_BETWEEN_CHECKS_FOR) # check again in PAUSE_BETWEEN_CHECKS_FOR seconds
                    else:
                        if temp == MAX_TEMP:
                            if get_state() == 'start_heater':
                                system_reset()
                                change_state('monitor_only')
                                threaded_timer = delayed_stop(system_reset, PAUSE_BETWEEN_CHECKS_FOR) # check again in PAUSE_BETWEEN_CHECKS_FOR seconds

                                log("Temperature (" + str(temp) + ") is perfect")
            except:
                kill()

    except KeyboardInterrupt:
        kill()
