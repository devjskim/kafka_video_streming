import cv2
import numpy as np
import os
from os.path import isfile, join
import time

pathIn = './image'
pathOut = 'output.avi'
fps = 10
fourcc = cv2.cv.CV_FOURCC(*'DIVX')
#fourcc = cv2.cv.CV_FOURCC('M','J','P','G')
#fourcc = cv2.VideoWriter_fourcc(*'DIVX')

frame_array = []
#files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
files = os.listdir(pathIn)
#files.sort()
files.sort()


for i in range(len(files)):
	print(files[i])

#files.sort(key = lambda x: x[5:-4])
#files.sort()

for i in range(len(files)):
	filename = pathIn + '/' + files[i]
	img = cv2.imread(filename,0)
	if not img.data:
		print("error during read images")
		break
	#height = np.size(img,0)
	#width = np.size(img,1)
	height = 480
	width = 640
	size = (width, height)

	frame_array.append(img)
	
	cv2.imshow('frame',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
	time.sleep(1/3)


out = cv2.VideoWriter(pathOut,fourcc, fps, size)
#out = cv2.VideoWriter(pathOut, -1, 1, size)


for i in range(len(frame_array)):
	out.write(frame_array[i])

out.release()
