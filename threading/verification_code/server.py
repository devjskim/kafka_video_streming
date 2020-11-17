import socket
from threading import *
import time
import numpy as np
import os, sys
import cv2

def recv_filenamelist(c_sock, filename_list):
	while True:
		file_name = c_sock.recv(40)
		if file_name.decode() == 'end':
			break
		else:
			filename_list.append(file_name)
			print(file_name)
	time.sleep(0.1)

def recv_frames(c_sock, path, filename_list):
	for i in range(len(filename_list)):
		data = c_sock.recv(65507)
		if data:
			array = np.frombuffer(data, dtype=np.dtype('uint8'))
			img = cv2.imdecode(array,1)
			cv2.imwrite(path+filename_list[i], img)
			print(filename_list[i])
		else:
			pass
		time.sleep(0.1)

if __name__ == "__main__":
	pathOut = "/home/pi5/image/"
	host = "10.0.1.11"
	port = 12345
	addr = (host,port)
	
	s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s_sock.bind(addr)
	s_sock.listen(5)

	c_sock, c_addr = s_sock.accept()
	
	print("client addr: ", c_addr)

	name_list = []

	recv_filenamelist(c_sock, name_list)
	recv_frames(c_sock, pathOut, name_list)
	
	c_sock.close()
	s_sock.close()
