#!/usr/bin/python3
import RPi.GPIO as GPIO
import logging
from RPLCD.i2c import CharLCD

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

def get_temp():
    current_temp = None

    if read("28-021892458db6") != None:
        current_temp = read("28-021892458db6")

    return current_temp

### code for running the pumps and heater

def start_heater():
    relay_on(RELAY_3)

def stop_heater():
    relay_off(RELAY_3)

def relay_on(pin):
    GPIO.output(pin, GPIO.HIGH)

def relay_off(pin):
    GPIO.output(pin, GPIO.LOW)

def lcd_write(line_1, line_2):
        LCD.cursor_pos = (0,0)
        LCD.write_string(line_1.ljust(16))
        LCD.cursor_pos = (1,0)
        LCD.write_string(line_2.ljust(16))

def log(message):
    logging.info(message)

if __name__ == '__main__':
    try:
        GPIO.cleanup()

        logging.basicConfig(filename='./logs/controller.log', format='%(asctime)s: %(levelname)s: %(message)s', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')

        MAX_TEMP=104.0

        # LCD 16x2 i2c
        LCD = CharLCD('PCF8574', 0x27)

        # 4 channel relay, only using one relay to control the heater
        GPIO.setmode(GPIO.BCM)
        RELAY_3 = 25 # currently allocated to heater
        GPIO.setup(RELAY_3, GPIO.OUT)

        # get current temperature and turn on/off heater as necessary
        current_temp = get_temp()

        temp_readout = str(current_temp) + chr(223) + "F"
        state_readout = 'Error'

        if current_temp >= MAX_TEMP:
            stop_heater()

            if current_temp == 500.0:
                state_readout = 'Sensor Error'
                log("Sensor error, shutting down heater")
            else:
                state_readout = 'Monitoring Temp'
                log("Temperature is good, nothing to do")
        else:
            start_heater()
            state_readout = 'Heater On'
            log("Temperature is low, turning heater on")

        lcd_write(temp_readout, state_readout)

    except KeyboardInterrupt:
        GPIO.cleanup()
        quit()
