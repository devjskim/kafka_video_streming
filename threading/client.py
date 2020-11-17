import socket
import cv2
import os, sys
import time


def sendto_split(sock, non_list, checksum_list):
	print(non_list)
	sendto_list = non_list.decode().split(',')

	for i in range(len(sendto_list)):

		index = int(sendto_list[i])
		checksum_list[index] = 0

def check(name_checksum):
    flag = True
    for i in range(len(name_checksum)):
        if name_checksum[i] == 0:
            flag = False
            break
    return flag

def send_filename(sock, filename_list):
	'''
	for i in range(len(filename_list)):
		checksum_list.append(0)
	'''

	for i in range(len(filename_list)+1):
		if i < len(filename_list):
			sock.send(filename_list[i].encode())
		else:
			sock.send('end'.encode())
			break
		time.sleep(0.3)

def send_frame(sock, path, list1, checksum_list , encode_param):
	print("sending image start")
	time.sleep(0.3)
	for i in range(len(list1)):
		try:
			if checksum_list[i] == 0:
				cap = cv2.imread(path + list1[i])
				result, img = cv2.imencode('.jpg', cap, encode_param)
				sock.send(img.tobytes())
				print(path + list1[i])

			time.sleep(0.3)
		except Exception as e:
			print(e)
			pass
	'''
	if flag:
		print("sending image finished")
	else:
		print("sending image finished with error")
	'''

def Main():
	host = '203.237.53.160'
	port = 12345
	#path = '/Users/kimjuseong/image/'
	#path = '/Users/kimjuseong/image/'
	path = '/home/mooc/image/'
	
	'''
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((host,port))
	encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
	'''
	filename_list = os.listdir(path)
	filename_list.sort()
	for i in range(len(filename_list)):
		print(filename_list[i])
	'''
	checksum_list = []
	for i in range(len(filename_list)):
		checksum_list.append(0)

	send_filename(sock, filename_list)
	data = sock.recv(40)
	if data.decode() == 'ready':
		while not check(checksum_list):
			send_frame(sock, path, filename_list, checksum_list, encode_param)
			non_list = sock.recv(200)
			sendto_split(sock,non_list, checksum_list)
	'''

if __name__ == '__main__':
	Main()
