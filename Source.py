import cv2
import numpy as np

def diceRead(image,key):

	gray=rgb2gray(image)	#converting to gray image
	otsuTresh, img= cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)	#getting otsu threshold value using built-in openCV function
	binary= binarization(gray, otsuTresh)	#converting to binary image

	kernel=np.array([1,2,1,2,4,2,1,2,1])/16.0 #kernel for convolution

	kernelSize= kernel.shape[0]	#get kernel size
	kernelSqrt= int(np.sqrt(kernelSize))	#get square root of kernel size

	kernel=np.reshape(kernel, (kernelSqrt,kernelSqrt))	#reshape 1D numPy array to 2D numPy array

	blurred,canny,circles=None,None,None
	snap=False
	if key==ord("c"):	#if c is pressed, calculate and show convoluted image
		blurred= convolution(binary, kernel) #kernel convolution
		canny=impCanny(blurred, 0.33)
		number=findCircles(image, canny)
		font=cv2.FONT_HERSHEY_SIMPLEX
		string= ("{}{}".format("Liczba oczek: ", number))
		cv2.putText(image, string, (10,20), font, 0.75, (0,0,255), 2)
		cv2.imshow("Circles", image)
		cv2.imwrite('img2.jpg', image)

		snap=True

	return gray,binary,blurred,canny,circles,snap;

def rgb2gray(image):

	B = image[:, :, 0] #extract B channel
	G = image[:, :, 1] #extract G channel
	R = image[:, :, 2] #extract R channel

	gray = (0.3 * R + 0.59 * G + 0.11 * B) #luminosity function
	gray = gray.astype(np.uint8)	#converting to uint8 type
	return gray	#returning grayScale image

def binarization(image, level):

	binary=image>level # numpy > operator compares values and returns True/False matrix
	binary=binary*255  # multiplying True(1) and False(0) by 255 gets us 255 and 0 - white and black
	binary=binary.astype(np.uint8) #converting to uint8 type
	return binary

def convolution(image, kernel):

	border=int(kernel.shape[0]/2) #get border size
	height=image.shape[0]
	width=image.shape[1]

	convoluted=np.zeros_like(image) #create matrix with zeroes

	imageBorder=np.zeros((height+border*2,width+border*2))	#zero matrix with border
	imageBorder[border:-border,border:-border]= image	#writing image to matrix with border

	for j in range(width):
		for i in range(height):
			convoluted[i, j]=(kernel*imageBorder[i:i+kernel.shape[0], j:j+kernel.shape[1]]).sum()	#propagate kernel and calculate sum

	convoluted=convoluted.astype(np.uint8) #convert to uint8 type
	return convoluted

def impCanny(image, sigma):

	median= np.median(image)	#calculate median value of pixel intensity in image

	lower=int(max(0, (1.0-sigma)*median)) #lower value 
	upper=int(min(255, (1.0+sigma)*median))	#upper value
	canny=cv2.Canny(image,lower,upper) #return result- canny

	return canny

def findCircles(image, canny):

	contours, hierarchy=cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	circles=[]
	contourNumber=0

	for contour in contours:
		approx= cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour,True), True)
		area= cv2.contourArea(contour)

		if ((20<area<120)):
			#print(area)
			contourNumber=contourNumber+1
			circles.append(contour)


	cv2.drawContours(image, circles, -1, (0,255,0), 2)
	number= int(contourNumber/2)

	return number
