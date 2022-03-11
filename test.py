import numpy as np
import cv2
import os

# Setting to camera capture to camera resolution 480 x 640
cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

try:
	# Keep track of frames for debugging and image testing
	frames = 0

	if not os.path.exists("Tutorials/Frames/"):
		os.mkdir("Tutorials/Frames/")
		print("Created new directory for logging frames")

	# Start live feed
	while(frames >= 0):
   		# Read with the USB camera
		_,frame=cap.read()
		   
		frames += 1

   		# Convert to hsv deals better with lighting
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

   		# Red is on the upper and lower of hsv scale. Requires 2 ranges
		lower_red1 = np.array([0, 150, 20])
		upper_red1 = np.array([10, 255, 255])
		lower_red2 = np.array([160,100,20])
		upper_red2 = np.array([179,255,255])
		# Mask input image with upper and lower red ranges
		red_only1 = cv2.inRange(hsv, lower_red1, upper_red1)
		red_only2 = cv2.inRange(hsv, lower_red2 , upper_red2)
		red_only = red_only1 + red_only2

   		# Green is on the upper and lower of hsv scale. Requires 2 ranges
		lower_green = np.array([40, 100, 20])
		upper_green = np.array([75, 255, 255])
		# Mask input image with upper and lower green ranges
		green_only = cv2.inRange(hsv, lower_green , upper_green)

   		# Blue is on the upper and lower of hsv scale. Requires 2 ranges
		lower_blue = np.array([100, 100, 20])
		upper_blue = np.array([125, 255, 255])
		# Mask input image with upper and lower blue ranges
		blue_only = cv2.inRange(hsv, lower_blue , upper_blue)
		
		# Mask for kernel opening
		mask=np.ones((5,5),np.uint8)
		
		# Opening operation on red, green, or blue for denoising
		opening=cv2.morphologyEx(green_only, cv2.MORPH_OPEN, mask)

		# Run connected components algo to return all objects it sees.
		num_labels, labels, stats, centroids =cv2.connectedComponentsWithStats(opening,4, cv2.CV_32S)

		# Matrix showing labels for each pixel in the image
		b = np.matrix(labels)

		cv2.imshow("frame", frame)

		# Gets largest contours and finds a square
		contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		square = None

		try:
			contour = max(contours, key=cv2.contourArea)
			peri = cv2.arcLength(contour, True)
			approx = cv2.approxPolyDP(contour, 0.04*peri, True)
			square = True if len(approx) == 4 else False
		except:
			square = False

   	 
		if num_labels > 1 and square:

			print("Green square found")

			# Extracts the label of the largest none background component
			# and displays distance from center and image.
			max_label, max_size = max([(i, stats[i, cv2.CC_STAT_AREA]) for i in range(1, num_labels)], key = lambda x: x[1])
			
			# Get only pixels with max_label as high (1), rest zero
			seg = (b == max_label)

			# Convert data to binary image
			seg = np.uint8(seg)
			seg[seg > 0] = 255
			
			# Get distance from center
			#print('distance from center:', -1 * (320 - centroids[max_label][0]))

			# Log images for debugging
			#cv2.imwrite(f"Tutorials/Frames/data_{frames}.png", frame)
			#cv2.imwrite(f"Tutorials/Frames/seg_{frames}.png", seg)

			cv2.imshow("seg", seg)

		else:
			print("None")

		if cv2.waitKey(1)==27:
			break

# To stop video execution, track exception and exit
except KeyboardInterrupt:
	cv2.destroyAllWindows()
	print("Press Ctrl-C to terminate while statement")
	pass
