import cv2
import math
import cmath
# from cv2 import mean
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

def angle_between_points(p1, p2):
    d1 = p2[0] - p1[0]
    d2 = p2[1] - p1[1]
    if d1 == 0:
        if d2 == 0:  # same points?
            deg = 0
        else:
            deg = 0 if p1[1] > p2[1] else 180
    elif d2 == 0:
        deg = 90 if p1[0] < p2[0] else 270
    else:
        deg = math.atan(d2 / d1) / math.pi * 180
        lowering = p1[1] < p2[1]
        if (lowering and deg < 0) or (not lowering and deg > 0):
            deg += 270
        else:
            deg += 90
    return deg



# Uncomment als je een plaatje wil gebruiken
# path = './kleurdetectie/Testimage.png'
# img = cv2.imread(path)

# Uncomment als je de webcam wil gebruiken
cap = cv2.VideoCapture(0)
cap.set(3,720)
cap.set(4,480)

colorBoot = colorPunt = (0,255,0)

# cv2.namedWindow("Trackbars Boot")
# cv2.namedWindow("Trackbars Punt")
# cv2.resizeWindow("Trackbars Boot",640,240)
# cv2.resizeWindow("Trackbars Punt",640,240)

# cv2.createTrackbar("Hue min", "Trackbars Boot", 0, 179, empty)
# cv2.createTrackbar("Hue max", "Trackbars Boot", 179, 179, empty)
# cv2.createTrackbar("Sat min", "Trackbars Boot", 0, 255, empty)
# cv2.createTrackbar("Sat max", "Trackbars Boot", 255, 255, empty)
# cv2.createTrackbar("Val min", "Trackbars Boot", 0, 255, empty)
# cv2.createTrackbar("Val max", "Trackbars Boot", 255, 255, empty)
# cv2.createTrackbar("Hue min", "Trackbars Punt", 0, 179, empty)
# cv2.createTrackbar("Hue max", "Trackbars Punt", 179, 179, empty)
# cv2.createTrackbar("Sat min", "Trackbars Punt", 0, 255, empty)
# cv2.createTrackbar("Sat max", "Trackbars Punt", 255, 255, empty)
# cv2.createTrackbar("Val min", "Trackbars Punt", 0, 255, empty)
# cv2.createTrackbar("Val max", "Trackbars Punt", 255, 255, empty)

# 15 px/cm
bootX, bootY, bootW, bootH = 590, 390, 150, 95
puntX, puntY, puntW, puntH = 650, 360, 40, 40

meanBoot = [[0.00000000 , 0.00000000]]
meanPunt = [[0.00000000 , 0.00000000]]
while True:
    # Uncomment als je de webcam wil gebruiken
    ret, img = cap.read()

    img = cv2.flip(img, 1)
    img = cv2.flip(img, 0)
    imgHSV = cv2.cvtColor(img, COLOR_BGR2HSV)
    # h_min = cv2.getTrackbarPos("Hue min", "Trackbars Boot")
    # h_max = cv2.getTrackbarPos("Hue max", "Trackbars Boot")
    # s_max = cv2.getTrackbarPos("Sat max", "Trackbars Boot")
    # s_min = cv2.getTrackbarPos("Sat min", "Trackbars Boot")
    # v_max = cv2.getTrackbarPos("Val max", "Trackbars Boot")
    # v_min = cv2.getTrackbarPos("Val min", "Trackbars Boot")
    # h_max1 = cv2.getTrackbarPos("Hue max", "Trackbars Punt")
    # h_min1 = cv2.getTrackbarPos("Hue min", "Trackbars Punt")
    # s_min1 = cv2.getTrackbarPos("Sat min", "Trackbars Punt")
    # s_max1 = cv2.getTrackbarPos("Sat max", "Trackbars Punt")
    # v_min1 = cv2.getTrackbarPos("Val min", "Trackbars Punt")
    # v_max1 = cv2.getTrackbarPos("Val max", "Trackbars Punt")
        

    # lower = np.array([h_min,s_min,v_min])
    # upper = np.array([h_max,s_max,v_max])
    lower = np.array([24, 105, 152])
    upper = np.array([60, 255, 255])
    mask = cv2.inRange(imgHSV, lower, upper)
    # mask = cv2.bitwise_not(mask)

    # lower1 = np.array([h_min1,s_min1,v_min1])
    # upper1 = np.array([h_max1,s_max1,v_max1])
    lower1 = np.array([91, 134, 0])
    upper1 = np.array([124, 255, 255])
    mask1 = cv2.inRange(imgHSV, lower1, upper1)
    # mask1 = cv2.bitwise_not(mask1)


    
    imgResultBoot = cv2.bitwise_and(img, img, mask = mask)
    imgGrayBoot = cv2.cvtColor(imgResultBoot, COLOR_BGR2GRAY)
    imgResultPunt = cv2.bitwise_and(img, img, mask = mask1)
    imgGrayPunt = cv2.cvtColor(imgResultPunt, COLOR_BGR2GRAY)


    contours, hierarchy = cv2.findContours(imgGrayBoot, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours1, hierarchy1 = cv2.findContours(imgGrayPunt, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for i, c in enumerate(contours):     # boot    
        area = cv2.contourArea(c)
        
        if area < 200 or 100000 < area:
            continue
        
        # approx = cv2.approxPolyDP(c, 0.01* cv2.arcLength(c, True), True)
        # rotated = cv2.minAreaRect(approx)
        # approx = cv2.boxPoints(c, 0.01* cv2.arcLength(c, True), True)
        # cv2.drawContours(img, [approx], 0, (0,0,0), 5)
        # cv2.drawContours(img , rotated, -1, (0,0,0))
        # x, y, w, h = cv2.boundingRect(approx)
        # cv2.rectangle(img, ( , ), ( , ), (0,0,0), 5) # boot
        hull = cv2.convexHull(c, True)

        cv2.drawContours(img, hull, -1, (255,0,0), 3, 8);

        # cv2.drawContours(img, contours, -1, (0, 0, 255), 2)
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

        # print("x: "+ str(meanPunt[0][0])+ " , y: " + str(meanPunt[0][1]))
        if (puntX-puntW//2)<meanPunt[0][0]<(puntX+puntW//2) and (puntY-puntH//2)<meanPunt[0][1]<(puntY+puntH//2):
            colorPunt = (255,0,255)
        else:
            colorPunt = (0,255,0)


    cv2.rectangle(img, (bootX-bootW//2, bootY-bootH//2), (bootX+bootW//2, bootY+bootH//2), colorBoot, 5) # boot
    cv2.rectangle(img, (puntX-puntW//2, puntY-puntH//2), (puntX+puntW//2, puntY+puntH//2), colorPunt, 5) # punt
    cv2.arrowedLine(img, (int(meanBoot[0][0]), int(meanBoot[0][1])), (bootX, bootY), (0,0,255), 5)
    # horizontaal vector
    # print(meanBoot)
    lengte = str(int((bootX-int(meanBoot[0][0]))/15)) + " cm"
    # (bootX-int(meanBoot[0][0])/2)-
    cv2.putText(img, lengte, (int(meanBoot[0][0])+int((bootX - int(meanBoot[0][0]))/2), int(meanBoot[0][1])-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA, False)
    cv2.arrowedLine(img, (int(meanBoot[0][0]), int(meanBoot[0][1])), (bootX, int(meanBoot[0][1])), (0,0,255), 5)
    # verticaal vector
    cv2.arrowedLine(img, (int(meanBoot[0][0]), int(meanBoot[0][1])), (int(meanBoot[0][0]), bootY), (0,0,255), 5)
    # rotatie vector
    cv2.arrowedLine(img, (int(meanBoot[0][0]), int(meanBoot[0][1])), (int(meanPunt[0][0]), int(meanPunt[0][1])), (0,255,0), 3)
    
    # print(angle_between_points(p1, p2))
    # print()
    # print(meanBoot[0][0]-meanPunt[0][0])
    # print(meanBoot[0][1]-meanPunt[0][1])
    vector1 = np.array([meanBoot[0][0]-meanPunt[0][0], meanBoot[0][1]-meanPunt[0][1]])
    vector2 = np.array([1,0])
    a_phase = cmath.phase(complex(int(vector1[0]),int(vector1[1])))
    b_phase = cmath.phase(complex(1,0))
    temp = (((b_phase+cmath.pi) - a_phase) * 180 / cmath.pi)-25
    if(temp>180):
        temp = temp -360
    cv2.putText(img, str(int(temp)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA, False)
    # print((a_phase - b_phase) * 180 / cmath.pi) 


    cv2.imshow("Image", img)
    cv2.imshow("MaskBoot", mask)
    cv2.imshow("MaskPunt", mask1)
    # cv2.imshow("MaskResult", imgResultBoot)
    # cv2.imshow("Grayimage", imgGrayBoot)


    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
        break
