import socket
import sys


if len(sys.argv) != 2:
    print("usage:", sys.argv[0], "<command (options: start_filtration, stop_filtration, start_heater, stop_heater, system_reset, system_off, get_temp)>")
    sys.exit(1)

msg  = sys.argv[1]

HOST = '127.0.0.1'
PORT = 10000
s = socket.socket()
s.connect((HOST, PORT))

s.send(msg.encode('utf-8'))

response = s.recv(4096)

print(response.decode('utf-8'))

s.close()
sys.exit(0)
