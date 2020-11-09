from picamera.array import PiRGBArray 
from picamera import PiCamera
import time
import cv2
import numpy as np

#from test import output
from Source import *

camera=PiCamera()
camera.resolution=(224, 224)
camera.framerate=32
rawCapture= PiRGBArray(camera, size=(224, 224))

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):


	key=cv2.waitKey(1) & 0xFF	#reading key

	if key==ord("q"):	#if 'q' was pressed destroy opencv windows and break loop
		cv2.destroyAllWindows()
		break

	inputImg=frame.array.copy()	#copy frame array to image- 3dim array

	result=diceRead(inputImg, key)		#Source file

	if result==0:
		print("Kernel has to be n x n, where n%2!=0 and n>1")
		break
	else:

		cv2.imshow("Original",inputImg)
		#cv2.imshow("GrayScale",result[0])
		cv2.imshow("Binary",result[1])
		if result[5]==True:
			#cv2.imshow("Blurred",result[2])
			cv2.imshow("Canny", result[3])

	rawCapture.truncate(0)		#deleting current frame to draw next one


