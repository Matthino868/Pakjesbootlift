import cv2
import numpy as np
from cv2 import COLOR_BGR2HSV
from cv2 import COLOR_BGR2GRAY

def empty(self):
    pass

path = 'positieDetectie/vormpjes.png'
img = cv2.imread(path)
imgHSV = cv2.cvtColor(img, COLOR_BGR2HSV)
h, w, _ = img.shape
cx = w/2
cy = h/2

cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    imgHSV = cv2.cvtColor(img, COLOR_BGR2HSV)

    #de kleuren licht rood en donker rood
    lower = np.array([21, 139, 0])
    upper = np.array([39, 255, 255])

    mask = cv2.inRange(imgHSV, lower, upper)
    imgResult = cv2.bitwise_and(img, img, mask = mask)
    imgGray = cv2.cvtColor(imgResult, COLOR_BGR2GRAY)
    imgContour = cv2.Canny(imgGray,50,50)
    coord=cv2.findNonZero(mask)[1]
    coordx=coord[0, 0]
    coordy=coord[0, 1]

    if coordx < cx:
        print("Naar Links")
    elif coordx == cx:
        print("goed")
    elif coordx > cx:
        print("Naar Rechts")

    if coordy < cy:
        print("Naar Achter")
    elif coordy == cy:
        print("goed")
    elif coordy > cy:
        print("Naar Voren")

    cv2.imshow("Image", img)
    cv2.imshow("Mask", mask)
    cv2.imshow("MaskResult", imgResult)

    k = cv2.waitKey(200) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
        break