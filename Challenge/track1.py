# Import all necessary libraries
from random import sample
from cv2 import threshold
import numpy as np
import cv2
import RPi.GPIO as GPIO
import time

# Import the motor library
from RpiMotorLib import RpiMotorLib

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

# Video capture likely to be 0 or 1
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#Stepper Motor Setup
GpioPins = [18, 23, 24, 25]

# Declare a named instance of class pass a name and motor type
mymotortest = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")
# Min time between motor steps (ie max speed)
step_time = .002

#PID Gain Values (these are just starter values)
Kp = 0.003
Kd = 0.0001
Ki = 0.0001

# Error values
d_error = 0
sum_error = 0

# Stores past n-many errors, this is to measure confidence from the center to later break the loop
sample_size = 30
last_error = [0] * sample_size

# Get polygon or number of sides in object
def side_parameter(object_name):
    # Connect to database
    db = mysql.connect(host=db_host, user=db_user, passwd=db_pass, database=db_name)
    cursor = db.cursor()

    # Get HSV range and polygon sides
    cursor.execute("SELECT sides FROM objects WHERE object_name = '" + object_name + "';")
    result = cursor.fetchone()
    db.close()

    return result[0]

# Get hsv ranges
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

def object_in_frame(object_name):
    # Keep track of frames for debugging and image testing
    frames = 0

    # Start live feed. Break until ~90% of collected errors are within 20
    while(frames >= 0):
        # Read with the USB camera
        _, frame = cap.read()
        frames += 1

        # Image processing
        hsv_range = hsv_parameters(object_name, frame)
        mask = np.ones((5, 5), np.uint8)
        opening = cv2.morphologyEx(hsv_range, cv2.MORPH_OPEN, mask)
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(opening, 4, cv2.CV_32S)
        b = np.matrix(labels)

        cv2.imshow("frame", frame)

        if num_labels > 1:

            max_label, max_size = max([(i, stats[i, cv2.CC_STAT_AREA]) for i in range(1, num_labels)], key = lambda x: x[1])
            
            # Get only pixels with max_label as high (1), rest zero
            seg = (b == max_label)

            # Convert data to binary image
            seg = np.uint8(seg)
            seg[seg > 0] = 255

            cv2.imshow("seg", seg)


if __name__ == '__main__':
    object_in_frame("red_octagon")