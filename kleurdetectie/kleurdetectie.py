import cv2
import numpy as np
from cv2 import COLOR_BGR2HSV
from cv2 import COLOR_BGR2GRAY

def empty(self):
    pass

path = 'kleurdetectie/vormpjes.png'
img = cv2.imread(path)
imgHSV = cv2.cvtColor(img, COLOR_BGR2HSV)

cap = cv2.VideoCapture(0)



cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars",640,240)

cv2.createTrackbar("Hue min", "Trackbars", 0, 179, empty)
cv2.createTrackbar("Hue max", "Trackbars", 179, 179, empty)
cv2.createTrackbar("Sat min", "Trackbars", 0, 255, empty)
cv2.createTrackbar("Sat max", "Trackbars", 255, 255, empty)
cv2.createTrackbar("Val min", "Trackbars", 0, 255, empty)
cv2.createTrackbar("Val max", "Trackbars", 255, 255, empty)



while True:
    ret, img = cap.read()
    imgHSV = cv2.cvtColor(img, COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("Hue min", "Trackbars")
    h_max = cv2.getTrackbarPos("Hue max", "Trackbars")
    s_min = cv2.getTrackbarPos("Sat min", "Trackbars")
    s_max = cv2.getTrackbarPos("Sat max", "Trackbars")
    v_min = cv2.getTrackbarPos("Val min", "Trackbars")
    v_max = cv2.getTrackbarPos("Val max", "Trackbars")
        

    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])

    mask = cv2.inRange(imgHSV, lower, upper)
    imgResult = cv2.bitwise_and(img, img, mask = mask)
    imgGray = cv2.cvtColor(imgResult, COLOR_BGR2GRAY)
    imgContour = cv2.Canny(imgGray,50,50)

    cv2.imshow("Image", img)
    cv2.imshow("Mask", mask)
    cv2.imshow("MaskResult", imgResult)

    cv2.waitKey(1)
