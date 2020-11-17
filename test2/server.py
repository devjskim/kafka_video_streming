import socket
import cv2
import sys
import time
import numpy as np

host = '203.237.53.160'
port = 1080
path = "/home/mooc/image2/"
lat = "latency: "
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((host,port))
sock.listen(0)
client_sock, addr = sock.accept()
while True:
	file_name = client_sock.recv(40)
	print(file_name)
	time.sleep(0.3)
	data = client_sock.recv(65507)
	array = np.frombuffer(data, dtype=np.dtype('uint8'))
	img = cv2.imdecode(array,1)
	#stime = time.time()
	#latency = stime - float(send_time)
	#cv2.putText(img, text + str(latency) + "seconds",(0,100) ,cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (255,255,255))
	cv2.imshow('image',img)
	cv2.imwrite(path + file_name, img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

sock.close()
