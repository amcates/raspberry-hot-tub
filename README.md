My attempt to create a Raspberry PI hot tub controller for a 1980s Hot Springs SPA.

The reasoning for the way it runs is that pumps/sensors have been off lately.  I run the filtration pump first to get an accurate reading.  Otherwise, I don't think it would read correctly.  I will eventually modify this to continuously monitor.  For now it's on a sort of timer.

## Requirements/Installation

### For Hot Tub Controller (python)
* python 2.7 or above
* RPi.GPIO
* RPLCD
* Twilio (only if you want to script twilio_send.py to send SMS, requires .env file)

### Settings live in controller.py

* max and min temps
MAX_TEMP=104.0
MIN_TEMP=102.0

* how long do we wait between checks when the temperature is 104+
PAUSE_BETWEEN_CHECKS_FOR = 5400

* how long to cycle filtration before we check the temperature
CYCLE_FILTRATION_FOR = 5

* debounce time for push buttons
DEBOUNCE = 0.5

* Button used to turn filtration on/off
FILTRATION_BUTTON_GPIO = 26
FILTRATION_BUTTON = Button(FILTRATION_BUTTON_GPIO, debounce=DEBOUNCE)

* how long the heater will run under certain conditions, see def determine_action
LONG_RUN  = 7200
MED_RUN   = 5400
SHORT_RUN = 3600

* configuration for server listening for commands
MAX_LENGTH = 4096
PORT = 10000
HOST = '127.0.0.1'
TIMEOUT = 2
LISTEN = 10

* LCD 16x2 i2c
LCD = CharLCD('PCF8574', 0x27)

* 4 channel relay

RELAY_1 = 23 # currently allocated to filtration pump
RELAY_2 = 24 # currently allocated to circulation pump
RELAY_3 = 25 # currently allocated to heater
RELAY_4 = 12 # not currently used, issue with Raspberry PI and voltage

### For Rails Server
* Ruby 2.4.2
* Just bundle install (Gemfile)
* For Twilio (to use rails runner "Client.sms_status", requires twilio.env file)
* Using Ratchet (goratchet.com) so it's designed to be viewed on mobile devices but will work on normal web browser
* Using Canvas Gauges (canvas-gauges.com)

git clone https://github.com/amcates/raspberry-hot-tub.git

## Usage

Normal operation:
python3 controller.rb

Rails server:
Located in rails_server folder
rails s -b 0.0.0.0 (development mode but available on your entire internal network, use some sort of web server if you want to make it more stable)

Cronjobs to start controller and server:
@reboot /bin/bash -l -c 'cd /location-of-application-folder python3 controller.py &'
@reboot /bin/bash -l -c 'cd /location-of-application-folder/rails_server && rails s -b 0.0.0.0 &'

To stop a background controller process, touch shutdown.txt from the application folder
