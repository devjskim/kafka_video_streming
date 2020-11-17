import io
import time
from PIL import Image
import datetime
import os
import cv2

cap = cv2.VideoCapture(0)

if(cap.isOpened() == False):
	print("Unable to read camera feed")

img_counter = 0

imageFolder = '/home/mooc/image/'
frame_numer = 0
for i in range(100):
    img_counter = 0
    path = imageFolder + "frame" + str(i)
    if not os.path.exists(path):
            os.makedirs(path)
    for j in range(100):
    	    now = datetime.datetime.now()
	    a = now.strftime("-%y-%m-%d-%H-%M-%S-")
	    start_time = time.time()
            ret, frame = cap.read()
	#cv2.imshow("test", frame)
	#if not ret:
	#	break
	#k = cv2.waitKey(1)

	    img_name = path + "/frames"+str(j).zfill(3)+".jpg"

	    cv2.imwrite(img_name, frame)
	#print("{} wirtten!".format(img_name))
	    img_counter += 1
	
	    time.sleep(0.1)
	    print("--- %s second ---" % (time.time() - start_time))

cap.release()
cv2.destroyAllWindows()
