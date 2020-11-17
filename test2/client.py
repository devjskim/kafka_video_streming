#!/usr/bin/env python
# coding: utf-8


# For debugging :
# - run the server and remember the IP of the server
# And interact with it through the command line:
# echo -n "get" > /dev/udp/192.168.0.39/1080
# echo -n "quit" > /dev/udp/192.168.0.39/1080

import socket
import cv2
import os
import sys
from threading import Thread, Lock
import sys
import time
from kafka import KafkaProducer


debug = True
jpeg_quality = 90
host = '203.237.53.160'
port = 1080
topic = "image-sample"
path = "/home/mooc/image/"

class VideoGrabber(Thread):
        """A threaded video grabber.
        
        Attributes:
        encode_params (): 
        cap (str): 
        attr2 (:obj:`int`, optional): Description of `attr2`.
        
        """
        def __init__(self, jpeg_quality):
                """Constructor.

                Args:
                jpeg_quality (:obj:`int`): Quality of JPEG encoding, in 0, 100.
                
                """
                Thread.__init__(self)
                self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality]
                self.cap = cv2.VideoCapture(0)
                self.running = True
                self.buffer = None
                self.lock = Lock()

        def stop(self):
                self.running = False
		self.cap.release()

        def get_buffer(self):
                """Method to access the encoded buffer.

                Returns:
                np.ndarray: the compressed image if one has been acquired. None otherwise.
                """
                if self.buffer is not None:
                        self.lock.acquire()
                        cpy = self.buffer.copy()
                        self.lock.release()
                        return cpy
                
        def run(self):
                while self.running:
                        success, img = self.cap.read()
                        if not success:
                                continue
                        
                        # JPEG compression
                        # Protected by a lock
                        # As the main thread may asks to access the buffer
                        self.lock.acquire()
                        result, self.buffer = cv2.imencode('.jpg', img, self.encode_param)
                        self.lock.release()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host,port))
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
list1 = os.listdir(path)
list1.sort()
while True:
	for i in range(len(list1)):
		cap = cv2.imread(path+list1[i])
		sock.send(list1[i])
	time.sleep(0.3)
#cv2.imshow('image', cap)
	result, img = cv2.imencode('.jpg', cap, encode_param)
	#if cv2.waitKey(0) & 0xFF == ord('q'):
	#	break
	sock.send(img.tobytes())
	time.sleep(0.1)
sock.close()
#cv2.waitKey(1)



#saock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
#address = (host, port)

#print('starting up on %s port %s\n' % server_address)

'''
while(running):
        #data, address = sock.recvfrom(4)
	data = "get"
	try:
        	if(data == "get"):
                	buffer = grabber.get_buffer()
	                if buffer is None:
        	                continue
                	if len(buffer) > 65507:
	                        print("The message is too large to be sent within a single UDP datagram. We do not handle splitting the message in multiple datagrams")
                	        continue
                # We sent back the buffer to the client
	                #sock.sendto(buffer.tobytes(), address)
			producer.send(topic, buffer.tobytes())
	#		print("sended")
        	elif(data == "quit"):
                	grabber.stop()
	                running = False
	except KeyboardInterrupt:
		grabber.stop()
		running = False
		break
 	time.sleep(0.3)
       
print("Quitting..")
grabber.join()
'''
