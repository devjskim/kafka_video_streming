import time
import os
from kafka import *

topic = "time-test"
key = "SHINEE KEY"
data = "lucifer"
path = "/home/mooc/img1"
consumer = KafkaConsumer(topic, bootstrap_servers=['192.168.0.100:9090'], auto_offset_reset = 'earliest')
consumer.subscribe(topic)
consumer.poll()
consumer.seek_to_end()
for msg in consumer:
	#print("{}, {}, {}".format(msg.key, msg.timestamp, msg.value))
	#print(msg)
	#str1 = msg.value.split(',')
	#print("{}, {}".format(str1[0], str1[2]))
	img = base64.b64decode(msg.value)
	key = 0
        #img = base64.b64decode(msg)
        cv2.imwrite(path+"frame"+str(key),img)
        print(path+"frame"+str(key))
        key += 1

