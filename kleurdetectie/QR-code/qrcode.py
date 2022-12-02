import cv2
img=cv2.imread("C:/Users/arthu/Pictures/QRcodes/BetaQR.png")
det=cv2.QRCodeDetector()
retval, decoded_info, points, straight_qrcode = det.detectAndDecodeMulti(img)
print(retval)
print(decoded_info)
print(points)

for i in points[0]:
    # print(type(i))
    # print(i[0])
    # x, y = i[0] , i[1]
    # print(x,  y)
    cv2.circle(img, (int(i[0]), int(i[1])), 3, (255, 0, 255), 5)
    


cv2.imshow("image", img)
k = cv2.waitKey(10000) & 0xFF
# if k == 27:
#     cap.release()
#     cv2.destroyAllWindows()
#     break
# cap.release()
cv2.destroyAllWindows()
# print(straight_qrcode)