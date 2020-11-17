import socket
import time
import datetime
import os

host = '203.237.53.160'
port = 1080
msg = 'say hello'
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((host,port))

text, server = sock.recvfrom(40)

print(server)
print(text)

time.sleep(1)

sock.sendto(msg, server)

