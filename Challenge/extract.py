from curses.ascii import isalnum
import cv2
import numpy as np
import pytesseract

def filter():
    img = cv2.imread('public/images/frame.png')
    image_bgr = cv2.imread('public/images/frame_grey.png')

    # convert to gray
    gray = cv2.cvtColor(image_bgr,cv2.COLOR_BGR2GRAY)

    # get largest contour
    contours = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    big_contour = max(contours, key=cv2.contourArea)

    cv2.drawContours(image_bgr, [big_contour], 0, (255, 255, 255), -1)

    result = cv2.bitwise_and(image_bgr, img, mask=None)

    return result

def get_text():
    img = filter()

    try:
        text = pytesseract.image_to_string(img, config='--psm 13')
        text = text.strip()
    except:
        text = ''
    
    return text

if __name__ == '__main__':
    print(get_text())