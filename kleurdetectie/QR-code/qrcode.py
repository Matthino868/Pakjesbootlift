import cmath
import time
import cv2
import numpy as np
print("Stream wordt geopend!")
# cap = cv2.VideoCapture("C:/school/Vakken/Project56/demofilmpjeFinal.MP4")
cap = cv2.VideoCapture(1)
first_time = True
prev_frame_time = 0 
new_frame_time = 0
ret, img = cap.read()

def angle_between(v1, v2):
    v1_u = v1 / np.linalg.norm(v1)
    v2_u = v2 / np.linalg.norm(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def fps_counter():
    global prev_frame_time
    global new_frame_time
    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    return str(int(fps))

while cap.isOpened():
# while True:
    ret, img = cap.read()
    if ret == False:
        continue
    img = cv2.resize(img, (1280,720))
    fps = fps_counter()

    retval, decoded_info, points, straight_qrcode = cv2.QRCodeDetector().detectAndDecodeMulti(img)
    x0, y0 = 1, 1
    x1, y1 = 0, 0
    kleur = (0,255,0)
    bootW = 150
    bootH = 150
    bootX = 950
    bootY = 450
    if retval:
        if first_time:
            print("De last mile carrier krijgt een bericht!")
            first_time = False
        for idlijst, i in enumerate(points):
            naam = decoded_info[idlijst].strip()
            a = np.array(i, np.int32)
            cv2.putText(img, naam, (int(i[0][0]),int(i[0][1])- 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA, False)
            cv2.polylines(img, [a], True,(0,255,255),5)
            
            if naam == "Beta":
                x0 = int((i[2][0]-i[0][0])//2 + i[0][0])
                y0 = int((i[2][1]-i[0][1])//2 + i[0][1])
                x1 = int((i[1][0]-i[0][0])//2 + i[0][0])
                y1 = int((i[1][1]-i[0][1])//2 + i[0][1])

                vector1 = np.array([x1-x0, y1-y0])
                vector2 = np.array([1,0])
                cv2.arrowedLine(img, (x0,y0), (x1,y1), (0,0,255), 5)
                hoek = np.degrees(angle_between(vector1,vector2))
                cv2.putText(img, str(int(hoek)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA, False)
                if abs(bootX-x0) < 50 and abs(bootY-y0) < 50 and hoek < 10:
                    kleur = (255,0,255)

                # Horizontale lijn
                horLengte = bootX - x0
                horPositie = x0 + (horLengte//2)
                cv2.putText(img, str(int(horLengte/25))+ " cm", (horPositie, y0 - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA, False)
                cv2.arrowedLine(img, (x0, y0),(bootX, y0),(0,255,255),2)
                # Verticale lijn
                verLengte = bootY-y0
                verPositie = y0 + (verLengte//2)
                cv2.putText(img, str(int(verLengte/25))+ " cm", (x0 + 30, verPositie), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA, False)
                cv2.arrowedLine(img, (x0, y0),(x0, bootY),(0,255,255),2)

    # cv2.putText(img, fps, (210, 80), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
        
    cv2.rectangle(img, (600,275),(1200,375),kleur,2)
    cv2.rectangle(img, (600,525),(1200,625),kleur,2)
    cv2.rectangle(img, (bootX-bootW//2, bootY-bootH//2), (bootX+bootW//2, bootY+bootH//2), kleur, 2) # boot

    # img = cv2.resize(img, (720,480))
    cv2.imshow("Image", img)
    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        #cap.release()
        cv2.destroyAllWindows()
        break
cap.release()
cv2.destroyAllWindows()