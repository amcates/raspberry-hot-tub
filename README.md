My attempt to create a Raspberry PI hot tub controller for a 1980s Hot Springs SPA.

The reasoning for the way it runs is that pumps/sensors have been off lately.  I run the filtration pump first to get an accurate reading.  Otherwise, I don't think it would read correctly.  I will eventually modify this to continuously monitor.  For now it's on a sort of timer.

## Heat Mode (we want 104)

1. run filtration pump (main pump for 20 seconds)
2. read input from temperature sensors
3. decide whether heater needs to be on/off (104 or greater don't run at all)
4. if 'on' then turn on circulation pump first (2 seconds before heater), then turn on heater
5. if 'off' then go to step 8
6. run heater for a set amount of time based on starting temperature (100-103 degrees = 20 min, 98-100 = 1hr, <98 = 1.5 hr)
7. start over at step 1
8. wait 1.5 hrs then repeat step 1

## Away Mode (we want 98) *** NOT YET IMPLEMENTED

1. run filtration pump (main pump for 20 seconds)
2. read input from temperature sensors
3. decide whether heater needs to be on/off (98 or greater don't run at all)
4. if 'on' then turn on circulation pump first (2 seconds before heater), then turn on heater
5. if 'off' then go to step 8
6. run heater for 20 min
7. start over at step 1
8. wait 1.5 hrs then repeat step 1


## Requirements/Installation

### For Hot Tub Controller (python)
* python 2.7 or above
* RPi.GPIO
* RPLCD
* Twilio (only if you want to script twilio_send.py to send SMS, requires .env file)

### For Rails Server
* Ruby 2.4.2
* Just bundle install (Gemfile)
* For Twilio (to use rails runner "Client.sms_status", requires twilio.env file)
* Using Ratchet (goratchet.com) so it's designed to be viewed on mobile devices but will work on normal web browser
* Using Canvas Gauges (canvas-gauges.com)

git clone https://github.com/amcates/raspberry-hot-tub.git

## Usage

Normal operation:
python controller.rb

Test mode:
TEST_MODE=true python controller.rb

Rails server:
Located in rails_server folder
rails s -b 0.0.0.0 (development mode but available on your entire internal network, use some sort of web server if you want to make it more stable)

