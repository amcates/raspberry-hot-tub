############################################################################
###### This should be run as cronjob at whatever interval you desire #######
############################################################################

import os
import socket
import sys
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

HOST = '127.0.0.1'
PORT = 10000

# get_temp
clientsocket = socket.socket()
clientsocket.connect((HOST, PORT))

clientsocket.send('get_temp'.encode('utf-8'))

current_temp = clientsocket.recv(4096).decode('utf-8')

# get_state

clientsocket.send('get_state'.encode('utf-8'))

current_state = clientsocket.recv(4096).decode('utf-8')

# send sms
message = f'Current Temp: {current_temp}\nCurrent State: {current_state}'

# Your Account SID from twilio.com/console
account_sid = os.getenv("SID")
# Your Auth Token from twilio.com/console
auth_token  = os.getenv("AUTH_TOKEN") 

client = Client(account_sid, auth_token)

message = client.messages.create(
    to=os.getenv("SMS_TO"),
    from_=os.getenv("SMS_FROM"),
    body=message)

print(message.sid)

clientsocket.close()
sys.exit(0)

