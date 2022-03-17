import numpy as np
import cv2
import os

# Import all MySQL libraries
import mysql.connector as mysql
from dotenv import load_dotenv
import os

# Loads all details from the "credentials.env"
load_dotenv('Challenge/credentials.env')
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

# Setting to camera capture to camera resolution 480 x 640
cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def hsv_parameters(object_name, frame):

    # Convert to hsv deals better with lighting
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_ranges = 0

    # Connect to database
    db = mysql.connect(host=db_host, user=db_user, passwd=db_pass, database=db_name)
    cursor = db.cursor()

    # Get HSV range and polygon sides
    cursor.execute("SELECT hue_lower, hue_upper, saturation_lower, saturation_upper, brightness_lower, brightness_upper FROM objects WHERE object_name = '" + object_name + "';")
    result = cursor.fetchall()
    db.close()
    for i in result:
        hsv_lower = np.array(i[0::2])
        hsv_upper = np.array(i[1::2])
        hsv_ranges += cv2.inRange(hsv, hsv_lower, hsv_upper)

    return hsv_ranges

try:
	# Keep track of frames for debugging and image testing
	frames = 0

	# Start live feed
	while(frames >= 0):
   		# Read with the USB camera
		_,frame=cap.read()
		   
		frames += 1

   		# Convert to hsv deals better with lighting
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		green_only = hsv_parameters("green_square", frame)
		
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

			# Extracts the label of the largest none background component and displays distance from center and image.
			max_label, max_size = max([(i, stats[i, cv2.CC_STAT_AREA]) for i in range(1, num_labels)], key = lambda x: x[1])
			
			# Get only pixels with max_label as high (1), rest zero
			seg = (b == max_label)

			# Convert data to binary image
			seg = np.uint8(seg)
			seg[seg > 0] = 255
			
			# Get distance from center
			#print('distance from center:', -1 * (320 - centroids[max_label][0]))

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
