# Import image processing libraries
import cv2
import numpy as np
import pytesseract

# Overlays the greyscale and colored image to obtain only largest contour/object
def transform():
    # Read images from last saved frame
    img = cv2.imread('public/images/frame.png')
    shadow = cv2.imread('public/images/frame_grey.png')

    # Convert to gray
    gray = cv2.cvtColor(shadow, cv2.COLOR_BGR2GRAY)

    # Get largest contour
    contours = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    big_contour = max(contours, key=cv2.contourArea)

    # Fills in shape/object
    cv2.drawContours(shadow, [big_contour], 0, (255, 255, 255), -1)

    result = cv2.bitwise_and(img, shadow, mask=None)

    return result

def get_processing(img):
    # Convert to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Get largest contour
    contours = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    big_contour = max(contours, key=cv2.contourArea)

    # Bound/crop largest contour
    x, y, w, h = cv2.boundingRect(big_contour)

    # Output roi
    roi = img[y:y+h, x:x+w]
    return roi

# Returns extracted text
def get_text():
    # Gets processed image
    img = transform()
    img = get_processing(img)

    # Extract text
    try:
        text = pytesseract.image_to_string(img)
        text = text.strip()
    except:
        text = ''
    
    return text

if __name__ == '__main__':
    print(get_text())