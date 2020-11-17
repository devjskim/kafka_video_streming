import socket
import time
import io

host = '203.237.53.160'
port = 1080

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
msg = 'hello'
sock.sendto(msg,(host,port))

time.sleep(1)

msg1, server = sock.recvfrom(40)

print(server)
print(msg1)
