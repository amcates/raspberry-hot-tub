require 'socket'
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
end
    
