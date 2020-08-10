#!/usr/bin/python3

from squid import *

# debounce time for push buttons
DEBOUNCE = 0.5

# Button used to turn filtration on/off
FILTRATION_BUTTON_GPIO = 26
FILTRATION_BUTTON = Button(FILTRATION_BUTTON_GPIO, debounce=DEBOUNCE)

while 1:
    if FILTRATION_BUTTON.is_pressed():
        print('Button pushed')
