import socket
import numpy as np
import os
from os.path import isfile, join
import time
import cv2

def file_list(name_list):
	pathIn = "/home/pi5/js_example/video_example/image/"
	name_list = os.listdir(pathIn)
	name_list.sort()

def send_filenamelist(sock, filename_list):
	for i in range(len(filename_list)+1):
		if i < len(filename_list):
			sock.send(filename_list[i].encode())
		else:
			sock.send("end".encode())
			break
		time.sleep(0.1)

def send_frames(sock, filename_list, PathIn, encode_param):
	print("frame sending started")
	for i in range(len(filename_list)):
		print(pathIn + filename_list[i])
		try:
			cap = cv2.imread(pathIn + filename_list[i],3)
			result, img = cv2.imencode('.jpg', cap, encode_param)
			sock.send(img.tobytes())
			print(pathIn + filename_list[i])
		except Exception as e:
			print(e)
			pass
		time.sleep(0.1)

if __name__ == "__main__":
	pathIn = "/home/pi5/js_example/video_example/image/"
	encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),90]
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host="10.0.1.11"
	port=12345
	addr = (host,port)
	
	sock.connect(addr)
	
	name_list = os.listdir(pathIn)
        name_list.sort()
	
	send_filenamelist(sock, name_list)		
	send_frames(sock, name_list, pathIn, encode_param)
	
	sock.close()
