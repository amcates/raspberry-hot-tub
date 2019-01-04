import socket
import sys


HOST = '127.0.0.1'
PORT = 10000
s = socket.socket()
s.connect((HOST, PORT))

msg = input("Command To Send: ")
s.send(msg.encode('utf-8'))
s.close()
sys.exit(0)
