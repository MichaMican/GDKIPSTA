import cv2
import numpy as np


image = cv2.imread('C:/Users/Philivanei/Downloads/ShouldBeRedAndYellow_100.jpg')
height = image.shape[0]
width = image.shape[1]



output = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# search circles in image
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 2, round((1/5)*height),param1=15,param2=32,minRadius=round((1/6)*width),maxRadius=round((1/4)*width))

if circles is not None:
	# convert the (x, y) coordinates and radius of the circles to integers
	circles = np.round(circles[0, :]).astype("int")
	# loop over the (x, y) coordinates and radius of the circles
	for (x, y, r) in circles:
		# output: circle + rectangle as center
		cv2.circle(output, (x, y), r, (0, 255, 0), 4)
		cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
	

	cv2.imwrite('C:/Users/Philivanei/Downloads/circles_detected.JPG', np.hstack([image, output]))
	cv2.waitKey(0)
else:
	print("No Circles detected!")