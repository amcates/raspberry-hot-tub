require 'twilio-ruby'
require 'dotenv'
Dotenv.load("twilio.env")

location = '/sys/bus/w1/devices/28-021892458db6/w1_slave'

lines = IO.readlines(location)
last_line = lines.last

raw_temp = last_line.split("=").last.gsub("\n", "")
temp_readout = (raw_temp.to_f/1000.0 * 1.8) + 32
temp_readout += 3 # adding offset

current_temp = temp_readout.round(2)

# only send SMS message if temp is greater than 105.0
if current_temp >= 105.0
  message = "Current Temp: #{current_temp}°F"

  account_sid = ENV['SID']
  auth_token = ENV['AUTH_TOKEN']
  sms_to = ENV['SMS_TO']
  sms_from = ENV['SMS_FROM']

  @client = Twilio::REST::Client.new account_sid, auth_token

  @client.api.account.messages.create(
    from: sms_from,
    to: sms_to,
    body: message
  )
end
