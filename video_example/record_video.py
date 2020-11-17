import cv2
import numpy as np

cap = cv2.VideoCapture(0)

if (cap.isOpened() == False):
	print("Unable to read camera feed")

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fourcc = cv2.cv.CV_FOURCC(*'XVID')
#out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
out = cv2.VideoWriter('outpy.avi',fourcc, 10, (frame_width,frame_height))

while(True):
        ret, frame = cap.read()

        if ret == True:
		out.write(frame)
                cv2.imshow('Frame', frame)

                if cv2.waitKey(25) & 0xFF == ord('q'):
                        break
        else:
                break

cap.release()
out.release()

cv2.destroyAllWindows()

