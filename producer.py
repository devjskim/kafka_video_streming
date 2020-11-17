#!/usr/bin/env python
# coding: utf-8


# For debugging :
# - run the server and remember the IP of the server
# And interact with it through the command line:
# echo -n "get" > /dev/udp/192.168.0.39/1080
# echo -n "quit" > /dev/udp/192.168.0.39/1080

import socket
import cv2
import sys
from threading import Thread, Lock
import sys
import time
import base64
from kafka import KafkaProducer
import os

#if(len(sys.argv) != 2):
#        print("Usage : {} interface".format(sys.argv[0]))
#        print("e.g. {} eth0".format(sys.argv[0]))
#        sys.exit(-1)


def get_ip(interface_name):
        """Helper to get the IP adresse of the running server
        """
        import netifaces as ni
        ip = ni.ifaddresses(interface_name)[2][0]['addr']
        return ip  # should print "192.168.100.37"

def send_frame(path, producer, topic):
	global data
	encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
	fname_list = os.listdir(path)
	fname_list = sorted(fname_list)
        for i in range(len(fname_list)):
                if i == len(fname_list):
                    print("append checksum")
                    producer.send(topic, b"checksum")
                else:
    		    read_im = cv2.imread(path+fname_list[i],1)
		    result, img = cv2.imencode('.jpg', read_im, encode_param)
		    producer.send(topic, img.tobytes())
		#cv2.imshow('read',read_im)
		#cv2.waitKey(10)
		    print(path + fname_list[i])
		    #if i < (len(fname_list)-1):
			    #data = "end"
		#if cv2.waitKey(1) & 0xFF == ord('q'):
		#	break
                time.sleep(0.1)

debug = True
jpeg_quality = 90
host = '192.168.50.100'
port = 1080
topic = "video"
key = "value"
data = "get"
path = "/home/mooc/image/frame"

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


#grabber = VideoGrabber(jpeg_quality)
#grabber.start()

running = True

producer = KafkaProducer(bootstrap_servers=['192.168.50.100:9092'])

#saock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
#address = (host, port)

#print('starting up on %s port %s\n' % server_address)


while(running):
        #data, address = sock.recvfrom(4)
        for i in range(100):
	    try:
	        if data == "get":
			'''
			buffer = grabber.get_buffer()
			if buffer is None:
				continue
			elif len(buffer) > 65507:
				print("the message is too long")
				continue
			'''
                        path_mod = path + str(i) + "/"
                        topic_mod = topic + str(i)
			#producer.send(topic, buffer.tobytes())
                        print("current path: " + path_mod)
                        print("current topic: " + topic_mod)
		        send_frame(path_mod, producer, topic_mod)
                        print("produce frame" + str(i) + " completed")
                        if i == 99:
                            data = "end"
	#		    print("sended")
        	elif data == "end":
	            running = False
		    break
	    except KeyboardInterrupt:
		running = False
                break
 	#time.sleep(0.1)
       
print("Quitting..")
#grabber.join()
