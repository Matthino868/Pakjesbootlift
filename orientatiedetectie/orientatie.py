import cv2
from cv2 import COLOR_BGR2HSV
from cv2 import COLOR_BGR2GRAY
import numpy as np
from math import atan2, cos, sin, sqrt, pi

def empty(self):
    pass

def drawAxis(img, p_, q_, color, scale):
    p = list(p_)
    q = list(q_)

    ## [visualization1]
    angle = atan2(p[1] - q[1], p[0] - q[0])  # angle in radians
    hypotenuse = sqrt((p[1] - q[1]) * (p[1] - q[1]) + (p[0] - q[0]) * (p[0] - q[0]))

    # Here we lengthen the arrow by a factor of scale
    q[0] = p[0] - scale * hypotenuse * cos(angle)
    q[1] = p[1] - scale * hypotenuse * sin(angle)
    cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)

    # create the arrow hooks
    p[0] = q[0] + 9 * cos(angle + pi / 4)
    p[1] = q[1] + 9 * sin(angle + pi / 4)
    cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)

    p[0] = q[0] + 9 * cos(angle - pi / 4)
    p[1] = q[1] + 9 * sin(angle - pi / 4)
    cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)
    ## [visualization1]

def getOrientation(pts, img):
    ## [pca]
    # Construct a buffer used by the pca analysis
    sz = len(pts)
    data_pts = np.empty((sz, 2), dtype=np.float64)
    for i in range(data_pts.shape[0]):
        data_pts[i, 0] = pts[i, 0, 0]
        data_pts[i, 1] = pts[i, 0, 1]

    # Perform PCA analysis
    mean = np.empty((0))
    mean, eigenvectors, eigenvalues = cv2.PCACompute2(data_pts, mean)

    # Store the center of the object
    cntr = (int(mean[0, 0]), int(mean[0, 1]))
    ## [pca]

    ## [visualization]
    # Draw the principal components
    cv2.circle(img, cntr, 3, (255, 0, 255), 2)
    p1 = (
        cntr[0] + 0.02 * eigenvectors[0, 0] * eigenvalues[0, 0],
        cntr[1] + 0.02 * eigenvectors[0, 1] * eigenvalues[0, 0],
    )
    p2 = (
        cntr[0] - 0.02 * eigenvectors[1, 0] * eigenvalues[1, 0],
        cntr[1] - 0.02 * eigenvectors[1, 1] * eigenvalues[1, 0],
    )
    drawAxis(img, cntr, p1, (255, 255, 0), 1)
    drawAxis(img, cntr, p2, (0, 0, 255), 5)

    angle = atan2(eigenvectors[0, 1], eigenvectors[0, 0])  # orientation in radians
    ## [visualization]

    # Label with the rotation angle
    label = "  Rotation Angle: " + str(-int(np.rad2deg(angle)) - 90) + " degrees"
    textbox = cv2.rectangle(
        img, (cntr[0], cntr[1] - 25), (cntr[0] + 250, cntr[1] + 10), (255, 255, 255), -1
    )
    cv2.putText(
        img,
        label,
        (cntr[0], cntr[1]),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 0, 0),
        1,
        cv2.LINE_AA,
    )

    return angle

# path = './vormpjes.png'
# img = cv2.imread(path)
# imgHSV = cv2.cvtColor(img, COLOR_BGR2HSV)

cap = cv2.VideoCapture(1)



cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars",640,240)

cv2.createTrackbar("Hue min", "Trackbars", 0, 179, empty)
cv2.createTrackbar("Hue max", "Trackbars", 179, 179, empty)
cv2.createTrackbar("Sat min", "Trackbars", 0, 255, empty)
cv2.createTrackbar("Sat max", "Trackbars", 255, 255, empty)
cv2.createTrackbar("Val min", "Trackbars", 0, 255, empty)
cv2.createTrackbar("Val max", "Trackbars", 255, 255, empty)


while True: 
    i = 0;
    ret, img = cap.read()
    imgHSV = cv2.cvtColor(img, COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("Hue min", "Trackbars")
    h_max = cv2.getTrackbarPos("Hue max", "Trackbars")
    s_min = cv2.getTrackbarPos("Sat min", "Trackbars")
    s_max = cv2.getTrackbarPos("Sat max", "Trackbars")
    v_min = cv2.getTrackbarPos("Val min", "Trackbars")
    v_max = cv2.getTrackbarPos("Val max", "Trackbars")
    
    
    print(h_min, h_max, s_min, s_max, v_min, v_max)

    # lower = np.array([h_min,s_min,v_min])
    # upper = np.array([h_max,s_max,v_max])
    # lower = np.array([0,27,220])
    # upper = np.array([50,255,255]) # Rood plaatje google
    # lower = np.array([90,98,136])
    # upper = np.array([167,255,255]) # Blauw
    # lower = np.array([0,3,4])
    # upper = np.array([8,255,255]) # Rood plaatje
    lower = np.array([3,126,112])
    upper = np.array([16,255,176]) # Oranje plaatje
    mask = cv2.inRange(imgHSV, lower, upper)
    imgResult = cv2.bitwise_and(img, img, mask = mask)
    imgGray = cv2.cvtColor(imgResult, COLOR_BGR2GRAY)
    imgContour = cv2.Canny(imgGray,50,50)
    contours, hierarchy = cv2.findContours(imgGray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for i, c in enumerate(contours):
        i = i + 1
        print(i)
        area = cv2.contourArea(c)
        if area < 3700 or 10000 < area:
            continue
        cv2.drawContours(imgGray, contours, -1, (0, 0, 255), 2)
        getOrientation(c, img)

    out = np.zeros_like(imgGray)
    cv2.drawContours(out, contours, -1, 255, 3)
    
    # 0 8 3 255 4 255
    
    cv2.imshow("test", img)
    cv2.imshow("mask", mask)
    cv2.imshow("imgResult", imgResult)
    cv2.imshow("imgContour", imgContour)
    cv2.imshow("imgGray", imgGray)
    cv2.imshow("imgcontours", out)
    
    
    cv2.waitKey(100)




