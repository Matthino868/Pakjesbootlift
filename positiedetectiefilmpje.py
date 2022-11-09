import cv2
import math
import cmath
from cv2 import COLOR_GRAY2RGB
import numpy as np
from cv2 import COLOR_BGR2HSV
from cv2 import COLOR_BGR2GRAY

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

def maakTrackbars(naam):
    cv2.namedWindow(naam)
    cv2.resizeWindow(naam, 640, 240)

    cv2.createTrackbar("Hue min", naam, 0, 179, empty)
    cv2.createTrackbar("Hue max", naam, 179, 179, empty)
    cv2.createTrackbar("Sat min", naam, 0, 255, empty)
    cv2.createTrackbar("Sat max", naam, 255, 255, empty)
    cv2.createTrackbar("Val min", naam, 0, 255, empty)
    cv2.createTrackbar("Val max", naam, 255, 255, empty)

def pakTrackbars(naam):
    minWaarde = []
    maxWaarde = []

    minWaarde.append(cv2.getTrackbarPos("Hue min", naam))
    maxWaarde.append(cv2.getTrackbarPos("Hue max", naam))
    minWaarde.append(cv2.getTrackbarPos("Sat min", naam))
    maxWaarde.append(cv2.getTrackbarPos("Sat max", naam))
    minWaarde.append(cv2.getTrackbarPos("Val min", naam))
    maxWaarde.append(cv2.getTrackbarPos("Val max", naam))
    waarde = [minWaarde,maxWaarde]
    return waarde

# Uncomment als je een plaatje wil gebruiken
# path = './kleurdetectie/Testimage.png'
# img = cv2.imread(path)

cap = cv2.VideoCapture("C:/Users/arthu/Desktop/testfilmpje.MP4")

# Uncomment als je de webcam wil gebruiken
# cap = cv2.VideoCapture(0)
cap.set(3,720)
cap.set(4,480)

colorBoot = colorPunt = (0,255,0)

# maakTrackbars("Trackbars Boot")
# maakTrackbars("Trackbars Punt")

cv2.namedWindow("Calibratie")
cv2.resizeWindow("Calibratie", 640, 50)
cv2.createTrackbar("Kalibratie", "Calibratie", 200, 399, empty)

# 15 px/cm
bootX, bootY, bootW, bootH = 590, 390, 150, 95
puntW, puntH = 40, 40
puntX, puntY = int(bootX + (bootW/2)-(puntW/2)), int(bootY - (bootH/2)+(puntH/2))

meanBoot = meanPunt = oudeMeanBoot =[[0.00000000 , 0.00000000]]
# img = cv2.flip(img, 1)
# img = cv2.flip(img, 0)
while cap.isOpened():
    ret, img = cap.read()
    if ret == False:
        continue
    img = cv2.resize(img, (720,480))

    imgHSV = cv2.cvtColor(img, COLOR_BGR2HSV)

    # bootWaarde = pakTrackbars("Trackbars Boot")
    # puntWaarde = pakTrackbars("Trackbars Punt")

    # lower = np.array(bootWaarde[0])
    # upper = np.array(bootWaarde[1])
    lower = np.array([24, 50, 50])
    upper = np.array([60, 255, 255])
    bootmask = cv2.inRange(imgHSV, lower, upper)
    # bootmask = cv2.bitwise_not(bootmask) # gebruik als iets zwart of rood is

    # lower1 = np.array(puntWaarde[0])
    # upper1 = np.array(puntWaarde[1])
    lower1 = np.array([91, 134, 0])
    upper1 = np.array([124, 255, 255])
    puntmask = cv2.inRange(imgHSV, lower1, upper1)
    # puntmask = cv2.bitwise_not(puntmask) # gebruik als iets zwart of rood is


    
    imgResultBoot = cv2.bitwise_and(img, img, mask = bootmask)
    imgGrayBoot = cv2.cvtColor(imgResultBoot, COLOR_BGR2GRAY)
    imgResultPunt = cv2.bitwise_and(img, img, mask = puntmask)
    imgGrayPunt = cv2.cvtColor(imgResultPunt, COLOR_BGR2GRAY)

    hull = []
    contours, hierarchy = cv2.findContours(imgGrayBoot, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours1, hierarchy1 = cv2.findContours(imgGrayPunt, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for i, c in enumerate(contours):     # boot    
        area = cv2.contourArea(c)
        
        if area < 8000 or 100000 < area:
            continue
        hull = hull.append(cv2.convexHull(c, True))

        cv2.drawContours(img, hull, -1, (255,0,0), 3, 8);

        cv2.drawContours(img, contours, -1, (0, 0, 255), 2)
        meanBoot = getOrientation(c, img)

        if (bootX-bootW//2)<meanBoot[0][0]<(bootX+bootW//2) and (bootY-bootH//2)<meanBoot[0][1]<(bootY+bootH//2):
            colorBoot = (255,0,255)
        else:
            colorBoot = (0,255,0)

    for v,b in enumerate(contours1): # punt
        area = cv2.contourArea(b)
            
        if area < 100 or 10000< area:
            continue

        #print(area)
        cv2.drawContours(img, contours1, -1, (0,255,255),2)
        meanPunt = getOrientation(b, img)

        if (puntX-puntW//2)<meanPunt[0][0]<(puntX+puntW//2) and (puntY-puntH//2)<meanPunt[0][1]<(puntY+puntH//2):
            colorPunt = (255,0,255)
        else:
            colorPunt = (0,255,0)
    
    temp = cv2.getTrackbarPos("Kalibratie", "Calibratie")
    realScale = 15/(temp+1)
    cv2.line(img, (50, 450), (50+temp, 450), (255,0,0), 1)
    if (meanBoot[0][0] != oudeMeanBoot[0][0]):

        cv2.rectangle(img, (bootX-bootW//2, bootY-bootH//2), (bootX+bootW//2, bootY+bootH//2), colorBoot, 2) # boot
        cv2.rectangle(img, (puntX-puntW//2, puntY-puntH//2), (puntX+puntW//2, puntY+puntH//2), colorPunt, 2) # punt
        # cv2.arrowedLine(img, (int(meanBoot[0][0]), int(meanBoot[0][1])), (bootX, bootY), (0,0,255), 5) # pijl van boot naar beste positie
        
        # horizontaal vector
        lengte = str(int((bootX-int(meanBoot[0][0]))*realScale)) + " cm"
        cv2.putText(img, lengte, (int(meanBoot[0][0])+int((bootX - int(meanBoot[0][0]))/2), int(meanBoot[0][1])-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA, False)
        cv2.arrowedLine(img, (int(meanBoot[0][0]), int(meanBoot[0][1])), (bootX, int(meanBoot[0][1])), (0,0,255), 5)
        
        # verticaal vector
        cv2.arrowedLine(img, (int(meanBoot[0][0]), int(meanBoot[0][1])), (int(meanBoot[0][0]), bootY), (0,0,255), 5)
        
        # rotatie vector
        cv2.arrowedLine(img, (int(meanBoot[0][0]), int(meanBoot[0][1])), (int(meanPunt[0][0]), int(meanPunt[0][1])), (0,255,0), 3)
        pijllengte = math.sqrt(pow(meanBoot[0][0]-meanPunt[0][0], 2) + pow(meanBoot[0][1]-meanPunt[0][1], 2))
        # print(pijllengte)
        vector1 = np.array([meanBoot[0][0]-meanPunt[0][0], meanBoot[0][1]-meanPunt[0][1]])
        vector2 = np.array([1,0])
        a_phase = cmath.phase(complex(int(vector1[0]),int(vector1[1])))
        b_phase = cmath.phase(complex(1,0))
        temp = (((b_phase+cmath.pi) - a_phase) * 180 / cmath.pi)-25

        if(temp>180):
            temp = temp -360
        cv2.putText(img, str(int(temp)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA, False)

    oudeMeanBoot = meanBoot

    bootmask = cv2.cvtColor(bootmask, COLOR_GRAY2RGB)
    puntmask = cv2.cvtColor(puntmask, COLOR_GRAY2RGB)

    puntmask = cv2.resize(puntmask, (360, 240))
    bootmask = cv2.resize(bootmask, (360, 240))
    v1 = np.vstack([img[:240], img[240:]])
    # 1080*480
    v2 = np.vstack([bootmask, puntmask])
    h1 = np.hstack([v1, v2])
    scale = 1.4
    h1 = cv2.resize(h1, (int(h1.shape[1]*scale), int(h1.shape[0]*scale)))
    # print(h1.shape[0])


    cv2.imshow("ImageStack", h1)

    # cv2.imshow("Image", img)
    # cv2.imshow("MaskBoot", bootmask)
    # cv2.imshow("MaskPunt", puntmask)
    # cv2.imshow("MaskResult", imgResultBoot)
    # cv2.imshow("Grayimage", imgGrayBoot)


    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        cap.release()
        cv2.destroyAllWindows()
        break
cap.release()
cv2.destroyAllWindows()