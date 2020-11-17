import socket
from threading import *
import time
import cv2
import numpy as np
import os, sys


def check(name_checksum):
    flag = True
    for i in range(len(name_checksum)):
        if name_checksum[i] == 0:
            flag = False
            break
    return flag

def sync_checksum(sock, name_checksum):
    non_list = ''
    for i in range(len(name_checksum)):
        if i < len(name_checksum) - 1 and name_checksum[i] == 1:
            non_list = non_list + str(i) + ','
        elif i == len(name_checksum) - 1:
            non_list = non_list + str(i)
    print(non_list)
    sock.send(non_list.encode())

def recv_filename(sock, name_list, name_checksum):
    while True:
        file_name = sock.recv(40)
        if file_name.decode() == 'end':
            break
        else:
            name_list.append(file_name.decode())
            name_checksum.append(0)


def recv_frame(sock, path, name_list, text,name_checksum):
    flag = False

    for i in range(len(name_list)):
        try:
            start_time = time.time()
            data = sock.recv(65507)
            if data:
                array = np.frombuffer(data, dtype=np.dtype('uint8'))
                img = cv2.imdecode(array, 1)
                #cv2.imshow('received', img)
                latency = time.time() - start_time
                #cv2.putText(img, text + str(latency) + "seconds",(0,100) ,cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (255,255,255))
                cv2.imwrite(path + name_list[i], img)
                print(latency)
                name_checksum[i] = 1
            else:
                pass
            time.sleep(0.3)

            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break

        except Exception as e:
            continue
    # flag = check(name_checksum)

def recv_result(mk_path, name_list, name_checksum):
    result_list = os.listdir(mk_path)
    result_list = sorted(result_list)

    for i in range(len(result_list)):
        for j in range(len(name_list)):
            if result_list[i] == name_list[j]:
                name_checksum[j] = 0
                break
            else:
                continue

# initialation phase

def handler(c_sock):
    index += 1
    path_in = index
    path = '/home/mooc/image'
    addr = (host, port)
    text = "latency: "
    name_list = []
    name_checksum = []
    mk_path = path + str(path_in) + '/'
    if os.path.exists(mk_path):
        f_list = os.listdir(mk_path)
	for f in f_list:
		os.unlink(f)	
    else:
        os.mkdir(mk_path, 777)

    print("client connected: ", addr[0],":",addr[1])
    recv_filename(c_sock, name_list, name_checksum)
    print("file name list received complete")
    print(name_list)
    c_sock.send('ready'.encode())

    while not check(name_checksum):
        recv_frame(c_sock, mk_path, name_list, text, name_checksum)
        #recv_result(mk_path, name_list, name_checksum)
        sync_checksum(c_sock, name_checksum)
    c_sock.close()

if __name__ == "__main__":
    index = 0
    host = '210.114.90.147'
    port = 12345
    addr = (host, port)
    flag = True
    global index


    s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_sock.bind(addr)
    s_sock.listen(5)
    print("wait for connecting...")
    while True:
        c_sock, c_addr = s_sock.accept()
        t = Thread(target=handler, args=(c_sock,))
        t.start()

