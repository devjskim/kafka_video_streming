from kafka import KafkaConsumer, TopicPartition
import io
import time
from PIL import Image
import datetime
import os
import cv2
import numpy as np
# settings
client = "192.168.50.100:9092"
topic = 'video'
path = "/home/mooc/videoexample/consumed/"
#consumer = KafkaConsumer(client)
consumer = KafkaConsumer(bootstrap_servers=client)

for i in range(100):
    topic_mod = topic + str(i)
    partitions = TopicPartition(topic_mod,0)
    consumer.assign([partitions])
#consumer = KafkaConsumer(client)
    consumer.seek_to_beginning()
    lastoffset = consumer.end_offsets([partitions])[partitions]
    path_mod = path + topic_mod + "/"
    print("topic name: " + topic_mod)
    print(lastoffset)
