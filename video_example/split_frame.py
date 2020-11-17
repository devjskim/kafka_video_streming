import cv2
import json

print(cv2.__version__)
vidcap = cv2.VideoCapture('outpy.avi')
success, image = vidcap.read()

count = 0
success = True

while success:
	num = str(count).zfill(3)
	cv2.imwrite("./image/frame%s.jpg" % num, image)
	success, image = vidcap.read()
	print 'read a new frame: ',success
	count += 1
