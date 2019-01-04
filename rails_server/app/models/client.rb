require 'socket'
class Client
  def self.send_msg(command)
    sock = TCPSocket.new('127.0.0.1', 10000)
    sock.send 'get_temp', 0
    response = sock.recv(4096) # Since the response message has 5 bytes.
    sock.close
    return JSON.parse(response)
  end
end
    
