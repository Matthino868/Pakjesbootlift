from bdb import GENERATOR_AND_COROUTINE_FLAGS
import cv2
from cv2 import mean
import numpy as np
from cv2 import COLOR_BGR2HSV
from cv2 import COLOR_BGR2GRAY

# from eigendetectie import getOrientation

def empty(self):
    pass

def getOrientation(pts, img):
    sz = len(pts)
    data_pts = np.empty((sz, 2), dtype=np.float64)
    for i in range(data_pts.shape[0]):
        data_pts[i, 0] = pts[i, 0, 0]
        data_pts[i, 1] = pts[i, 0, 1]
    
    mean = np.empty((0))
    mean, eigenvectors, eigenvalues = cv2.PCACompute2(data_pts, mean)
    center = (int(mean[0, 0]), int(mean[0, 1]))

    cv2.circle(img, center, 3, (255, 0, 255), 2)
    return mean

# Uncomment als je een plaatje wil gebruiken
# path = './vormpjes.png'
# img = cv2.imread(path)

# Uncomment als je de webcam wil gebruiken
cap = cv2.VideoCapture(0)

cap.set(3,720)
cap.set(4,480)

colorBoot = colorPunt = (0,255,0)

cv2.namedWindow("Trackbars Boot")
cv2.namedWindow("Trackbars Punt")
cv2.resizeWindow("Trackbars Boot",640,240)
cv2.resizeWindow("Trackbars Punt",640,240)

cv2.createTrackbar("Hue min", "Trackbars Boot", 0, 179, empty)
cv2.createTrackbar("Hue max", "Trackbars Boot", 179, 179, empty)
cv2.createTrackbar("Sat min", "Trackbars Boot", 0, 255, empty)
cv2.createTrackbar("Sat max", "Trackbars Boot", 255, 255, empty)
cv2.createTrackbar("Val min", "Trackbars Boot", 0, 255, empty)
cv2.createTrackbar("Val max", "Trackbars Boot", 255, 255, empty)
cv2.createTrackbar("Hue min", "Trackbars Punt", 0, 179, empty)
cv2.createTrackbar("Hue max", "Trackbars Punt", 179, 179, empty)
cv2.createTrackbar("Sat min", "Trackbars Punt", 0, 255, empty)
cv2.createTrackbar("Sat max", "Trackbars Punt", 255, 255, empty)
cv2.createTrackbar("Val min", "Trackbars Punt", 0, 255, empty)
cv2.createTrackbar("Val max", "Trackbars Punt", 255, 255, empty)

bootX, bootY, bootW, bootH = 345, 237, 150, 75
puntX, puntY, puntW, puntH = 425, 192, 130, 65

while True:
    # Uncomment als je de webcam wil gebruiken
    ret, img = cap.read()
    img = cv2.flip(img, 1)

    imgHSV = cv2.cvtColor(img, COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("Hue min", "Trackbars Boot")
    h_max = cv2.getTrackbarPos("Hue max", "Trackbars Boot")
    s_max = cv2.getTrackbarPos("Sat max", "Trackbars Boot")
    s_min = cv2.getTrackbarPos("Sat min", "Trackbars Boot")
    v_max = cv2.getTrackbarPos("Val max", "Trackbars Boot")
    v_min = cv2.getTrackbarPos("Val min", "Trackbars Boot")
    h_max1 = cv2.getTrackbarPos("Hue max", "Trackbars Punt")
    h_min1 = cv2.getTrackbarPos("Hue min", "Trackbars Punt")
    s_min1 = cv2.getTrackbarPos("Sat min", "Trackbars Punt")
    s_max1 = cv2.getTrackbarPos("Sat max", "Trackbars Punt")
    v_min1 = cv2.getTrackbarPos("Val min", "Trackbars Punt")
    v_max1 = cv2.getTrackbarPos("Val max", "Trackbars Punt")
        

    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    mask = cv2.inRange(imgHSV, lower, upper)
    mask = cv2.bitwise_not(mask)

    lower1 = np.array([h_min1,s_min1,v_min1])
    upper1 = np.array([h_max1,s_max1,v_max1])
    mask1 = cv2.inRange(imgHSV, lower1, upper1)
    # mask1 = cv2.bitwise_not(mask1)


    
    imgResultBoot = cv2.bitwise_and(img, img, mask = mask)
    imgGrayBoot = cv2.cvtColor(imgResultBoot, COLOR_BGR2GRAY)
    imgResultPunt = cv2.bitwise_and(img, img, mask = mask1)
    imgGrayPunt = cv2.cvtColor(imgResultPunt, COLOR_BGR2GRAY)


    contours, hierarchy = cv2.findContours(imgGrayBoot, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours1, hierarchy1 = cv2.findContours(imgGrayPunt, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for i, c in enumerate(contours):
        # for v, b in enumerate(contours1):
        
        area = cv2.contourArea(c)
        
        if area < 200 or 100000 < area:
            continue
        

        # print(area)
        cv2.drawContours(img, contours, -1, (0, 0, 255), 2)
        meanBoot = getOrientation(c, img)
        # meanPunt = getOrientation(b, img)

        # try:
        # print("x: "+ str(meanBoot[0][0])+ " , y: " + str(meanBoot[0][1]))
        # except:
        #     print("foutje")
        
        # x: 326.25 , y: 247.75 
        if (bootX-bootW//2)<meanBoot[0][0]<(bootX+bootW//2) and (bootY-bootH//2)<meanBoot[0][1]<(bootY+bootH//2):
            # if (puntX-puntW//2)<meanP
            colorBoot = 255,0,255
        else:
            colorBoot = 0,255,0

    for v,b in enumerate(contours1):
        area = cv2.contourArea(b)
            
        if area < 100 or 100000< area:
            continue
        
        cv2.drawContours(img, contours1, -1, (0,255,255),2)
        meanPunt = getOrientation(b, img)

        print("x: "+ str(meanPunt[0][0])+ " , y: " + str(meanPunt[0][1]))
        if (puntX-puntW//2)<meanPunt[0][0]<(puntX+puntW//2) and (puntY-puntH//2)<meanPunt[0][1]<(puntY+puntH//2):
            # if (puntX-puntW//2)<meanP
            colorPunt = 255,0,255
        else:
            colorPunt = 0,255,0

    

    cv2.rectangle(img, (bootX-bootW//2, bootY-bootH//2), (bootX+bootW//2, bootY+bootH//2), colorBoot, 5) # Punt
    cv2.rectangle(img, (puntX-puntW//2, puntY-puntH//2), (puntX+puntW//2, puntY+puntH//2), colorPunt, 5) # boot

    cv2.imshow("Image", img)
    cv2.imshow("Mask", mask)
    cv2.imshow("Mask1", mask1)
    cv2.imshow("MaskResult", imgResultBoot)
    cv2.imshow("Grayimage", imgGrayBoot)


    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
        break
