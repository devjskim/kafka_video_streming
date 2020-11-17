import time
import os
from kafka import *
import datetime
import cv2
import os
import base64

topic = "time-test"
key = "SHINEE KEY"
data = "lucifer"
producer = KafkaProducer(bootstrap_servers=['192.168.0.100:9090'])
path = "/home/mooc/image/"
list1 = os.listdir(path)
list1.sort()
for i in range(10):
#	producer.produce(topic,timestamp=datetime.datetime.now())
	cap = cv2.imread(path+list1[i])
	print(path+list1[i])
	msg = base64.b64encode(cap)
	#msg = key + ','+str1+','+str(time.time())
	producer.send(topic,msg)
	print('posted')
