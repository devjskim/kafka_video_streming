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

imageFolder = '/home/pi5/image/'
frame_numer = 0
while img_counter < 100:
	now = datetime.datetime.now()
	#a = now.strftime("-%y-%m-%d-%H-")
	start_time = time.time()
	ret, frame = cap.read()
	cv2.imshow("test", frame)
	if not ret:
		break
	k = cv2.waitKey(1)

	img_name = "{}opencv_frame_{}.jpg".format(imageFolder,img_counter)
	cv2.imwrite(img_name, frame)
	print("{} wirtten!".format(img_name))
	img_counter += 1
	
	time.sleep(0.3)
	print("--- %s second ---" % (time.time() - start_time))

cap.release()
cv2.destroyAllWindows()
