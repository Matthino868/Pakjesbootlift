import time
import cv2
import numpy as np
# img=cv2.imread("C:/Users/arthu/Pictures/QRcodes/AlphaQR.png")
cap = cv2.VideoCapture("C:/Users/arthu/Desktop/qrcodetestfilmpje.MP4")
# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m','j','p','g'))
# cap = cv2.VideoCapture(0)

# cap.set(3,720)
# cap.set(4,720)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 100)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)

prev_frame_time = 0 
new_frame_time = 0
ret, img = cap.read()

# sizeX = img.shape[1]
# sizeY = img.shape[0]

# print(int(sizeX-(sizeX*0.20)), int(sizeY-(sizeY*0.20)))

# bootX, bootY, bootW, bootH = int(sizeX-(sizeX*0.20)), int(sizeY-(sizeY*0.20)), int(sizeX*0.2), int(sizeY*0.2)
# puntW, puntH = 40, 40
# puntX, puntY = int(bootX + (bootW/2)-(puntW/2)), int(bootY - (bootH/2)+(puntH/2))

# print(dir(cap.get))

# while cap.isOpened():
while True:
    ret, img = cap.read()
    if ret == False:
        continue
    # img=cv2.imread("C:/Users/arthu/Pictures/QRcodes/eigenqr3.png")
    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    fps = str(int(fps))
    # print(img.shape, fps)

    # kernel = np.array([[0, -1, 0],
    #                [-1, 5,-1],
    #                [0, -1, 0]])
    # image_sharp = cv2.filter2D(src=img, ddepth=-1, kernel=kernel)
    # img = image_sharp

    img = cv2.resize(img, (1280,720))
    # img = cv2.resize(img, (720,480))
    # det=cv2.QRCodeDetector()
    retval, decoded_info, points, straight_qrcode = cv2.QRCodeDetector().detectAndDecodeMulti(img)

    if retval:
        # linksboven
        # cv2.circle(img, (int(points[0][0][0]), int(points[0][0][1])), 3, (255, 0, 255), 5)
        # rechtsboven
        # cv2.circle(img, (int(points[0][1][0]), int(points[0][1][1])), 3, (0, 0, 255), 5)
        # rechtsonder
        # cv2.circle(img, (int(points[0][2][0]), int(points[0][2][1])), 3, (255, 0, 0), 5)
        # linksonder
        # cv2.circle(img, (int(points[0][3][0]), int(points[0][3][1])), 3, (255, 255, 0), 5)

        for idlijst, i in enumerate(points):
            a = np.array(i, np.int32)
            cv2.putText(img, decoded_info[idlijst], (int(i[0][0]),int(i[0][1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA, False)
            cv2.polylines(img, [a], True,(0,255,255),5)

            x0 = int((i[2][0]-i[0][0])//2 + i[0][0])
            y0 = int((i[2][1]-i[0][1])//2 + i[0][1])
            x1 = int((i[1][0]-i[0][0])//2 + i[0][0])
            y1 = int((i[1][1]-i[0][1])//2 + i[0][1])

            cv2.arrowedLine(img, (x0,y0), (x1,y1), (0,0,255), 5)

    img = cv2.resize(img, (720,480))
    cv2.putText(img, fps, (210, 80), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
    sizeX = img.shape[1]
    sizeY = img.shape[0]

    # print(int(sizeX-(sizeX*0.20)), int(sizeY-(sizeY*0.20)))

    bootX, bootY, bootW, bootH = int(sizeX-(sizeX*0.20)), int(sizeY-(sizeY*0.20)), int(sizeX*0.2), int(sizeY*0.2)
    cv2.rectangle(img, (bootX-bootW//2, bootY-bootH//2), (bootX+bootW//2, bootY+bootH//2), (0,255,0), 2) # boot
    
    # image_sharp = cv2.resize(image_sharp, (720,480))
    # cv2.imshow('AV CV- Winter Wonder Sharpened', image_sharp)
    cv2.imshow("Image", img)
    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        #cap.release()
        cv2.destroyAllWindows()
        break
#cap.release()
cv2.destroyAllWindows()

# det=cv2.QRCodeDetector()
# retval, decoded_info, points, straight_qrcode = det.detectAndDecodeMulti(img)
# print(retval)
# print(decoded_info)
# print(points)

# for i in points[0]:
#     # print(type(i))
#     # print(i[0])
#     # x, y = i[0] , i[1]
#     # print(x,  y)
#     cv2.circle(img, (int(i[0]), int(i[1])), 3, (255, 0, 255), 5)
    


# cv2.imshow("image", img)
# k = cv2.waitKey(10000) & 0xFF
# # if k == 27:
# #     cap.release()
# #     cv2.destroyAllWindows()
# #     break
# # cap.release()
# cv2.destroyAllWindows()
# # print(straight_qrcode)