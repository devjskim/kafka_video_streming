#!/usr/bin/env python
# coding: utf-8

import socket
import cv2
import numpy as np
import sys
import time
from kafka import *
from PIL import Image
import io
import os
#if(len(sys.argv) != 3):
#    print("Usage : {} hostname port".format(sys.argv[0]))
#    print("e.g.   {} 192.168.0.39 1080".format(sys.argv[0]))
#    sys.exit(-1)


#cv2.namedWindow("Image")

# Create a UDP socket
#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '203.237.53.160'
port = 1080
address = (host, port)
topic = "video1"
path = "/home/mooc/image"
mk_path = "/home/mooc/img1/"
#os.mkdir(mk_path, 777)

def recv_frame(topic, value, path, key, starttime):
	#print(msg)
	array = np.frombuffer(value, dtype=np.dtype('uint8'))
	img = cv2.imdecode(array,1)
	#cv2.imshow('recv',img)
	#cv2.imwrite(path+str(key)+'.jpg', img)
	latency = starttime - time.time()
	print(latency)
	time.sleep(0.3)
key = 0
#sock.bind(address)
consumer = KafkaConsumer(topic, bootstrap_servers='192.168.0.100:9090', auto_offset_reset = 'earliest')
#partitions = consumer.poll(timeout)
while(True):
	consumer = KafkaConsumer(topic, bootstrap_servers='192.168.0.100:9090', auto_offset_reset = 'earliest')
	message = next(consumer)
	for msg in consumer:
	#for msg in message:
		if msg.value:
			#print(len(msg.value))
			#key = 0
			start_time = time.time()
			array = np.frombuffer(msg.value, dtype=np.dtype('uint8'))
			img = cv2.imdecode(array,1)
			#cv2.imshow('recv',img)
			cv2.imwrite(mk_path+"frame"+str(key).zfill(3)+'.jpg', img)
			key += 1
			'''
			cv2.waitKey(10)
			if cv2.waitKey(1) & 0xFF == ord('q'):
        			break
			'''
			lat = time.time() - start_time
			print("latency: {} seconds".format(lat))
			print("bandwidth: {} bytes/sec".format(len(msg.value)/lat))
		time.sleep(0.1)
	'''
	print('received')
	msg = next(consumer)
	key= cv2.waitKey(1) & 0xFF
	#image = Image.open(io.BytesIO(msg[6])).convert('RGB')
	image = Image.open(io.BytesIO(msg)).convert('RGB')
	img = np.array(image)
	cv2.imshow('recv',img)

	if key == ord("q"):
		break
	'''
