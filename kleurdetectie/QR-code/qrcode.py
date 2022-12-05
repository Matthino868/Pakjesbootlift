import cv2
img=cv2.imread("C:/Users/arthu/Pictures/QRcodes/eigenqr3.png")
# cap = cv2.VideoCapture("C:/Users/arthu/Downloads/Instructievideo.mp4")
# cap = cv2.VideoCapture(1)

# cap.set(3,1280)
# cap.set(4,720)

# while cap.isOpened():
while True:
    # ret, img = cap.read()
    # if ret == False:
    #     continue
    img=cv2.imread("C:/Users/arthu/Pictures/QRcodes/eigenqr3.png")

    # img = cv2.resize(img, (720,720))
    # print(points)
    det=cv2.QRCodeDetector()
    retval, decoded_info, points, straight_qrcode = det.detectAndDecodeMulti(img)
    # print(points)
    if retval:
        print(decoded_info)
        # print(straight_qrcode)
        for idlijst, i in enumerate(points):
            print(i)
            # print(i[0])
            cv2.putText(img, decoded_info[idlijst], (int(i[0][0]),int(i[0][1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA, False)
            cv2.rectangle(img, (int(i[0][0]),int(i[0][1])), (int(i[2][0]),int(i[2][1])), (255,0,0), 2) # punt
                
        # print(points[0][3])
        # print(points[0][0][0])
        # cv2.rectangle(img, (int(points[0][0][0]),int(points[0][0][1])), (int(points[0][2][0]),int(points[0][2][1])), (255,0,0), 2) # punt

        # for i in points[0]:
            # print(type(i))
            # print(i[0])
            # x, y = i[0] , i[1]
            # print(x,  y)
            # cv2.rectangle(img, (i[0], puntY-puntH//2), (puntX+puntW//2, puntY+puntH//2), colorPunt, 2) # punt
            # cv2.rectangle(img, (int(points[0][0][0]),int(points[0][0][1])), (int(points[0][2][0]),int(points[0][2][1])), (255,0,0), 2) # punt

            # cv2.circle(img, (int(i[0]), int(i[1])), 3, (255, 0, 255), 5)

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