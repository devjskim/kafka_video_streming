#!/usr/bin/env python
# coding: utf-8

import socket
import cv2
import numpy as np
import sys
import time

#if(len(sys.argv) != 3):
#    print("Usage : {} hostname port".format(sys.argv[0]))
#    print("e.g.   {} 192.168.0.39 1080".format(sys.argv[0]))
#    sys.exit(-1)


cv2.namedWindow("Image")

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '203.237.53.160'
port = 1080
address = (host, port)

sock.bind(address)

while(True):
    
    #sent = sock.sendto("get", address)

    data, server = sock.recvfrom(65507)
    print("Fragment size : {}".format(len(data)))
    if len(data) == 4:
        # This is a message error sent back by the server
        if(data == "FAIL"):
            continue
    array = np.frombuffer(data, dtype=np.dtype('uint8'))
    img = cv2.imdecode(array, 1)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("The client is quitting. If you wish to quite the server, simply call : \n")
print("echo -n \"quit\" > /dev/udp/{}/{}".format(host, port))
