import threading
import socket
from _thread import *

print_lock = threading.Lock()

def threaded(c):
    while True:

        data = c.recv(1024)

        if not data:
            print('bye')

            print_lock.release()
            break

        data = data[::-1]

        c.send(data)

    c.close()


def Main():
    host = "203.237.53.61"

    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket is binded to: ", host, " ", port)

    s.listen()
    print("socket is listening")

    while True:

        c,addr = s.accept()

        print_lock.acquire()
        print("Connected to: ", addr[0], ':', addr[1])

        start_new_thread(threaded,(c,))
    s.close()


if __name__ == "__main__":
    Main()
