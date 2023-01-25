import numpy as np
import pyboof as pb
import cv2

# Detects all the QR Codes in the image and prints their message and location
data_path = "C:/Users/arthu/Pictures/QRcodes/eigenqr2.png"
img=cv2.imread("C:/Users/arthu/Pictures/QRcodes/eigenqr2.png")


detector = pb.FactoryFiducial(np.uint8).microqr()

# detector = pb.QrCodeDetector()

image = pb.load_single_band(data_path, np.uint8)

detector.detect(image)

print("Detected a total of {} QR Codes".format(len(detector.detections)))

for qr in detector.detections:
    print("Message: " + qr.message)
    print("     at: " + str(qr.bounds))

print(type(qr.bounds))
bounds = qr.bounds.convert_tuple()
print(bounds)

cv2.rectangle(img, (int(bounds[0][0]),int(bounds[0][1])), (int(bounds[2][0]),int(bounds[2][1])), (255,0,0), 5) # punt


img = cv2.resize(img,(720,720))
cv2.imshow("image", img)

k = cv2.waitKey(10000) & 0xFF