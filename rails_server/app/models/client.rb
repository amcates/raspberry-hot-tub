require 'socket'
require 'twilio-ruby'
require 'dotenv'
Dotenv.load(Rails.root.join("twilio.env"))

class Client
  STATE_TRANSLATION = {'system_off' => ['System Off', 'btn-primary'], 
                       'None' => ['System Monitoring Temperature', 'btn-primary'], 
                       'monitor_only' => ['System Monitoring Temperature', 'btn-primary'], 
                       'start_filtration' => ['Jets On', 'btn-positive'], 
                       'start_heater' => ['Heater On', 'btn-negative']
  }

  def self.send_msg(command)
    sock = TCPSocket.new('127.0.0.1', 10000)
    sock.send command, 0
    response = sock.recv(4096)
    sock.close
    return response
  end

  def self.sms_status()
    current_temp = self.send_msg("get_temp")
    current_state = self.send_msg("get_state")

    message = "Current Temp: #{current_temp}°F \n Current State: #{STATE_TRANSLATION[current_state][0]}"

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
end
    
