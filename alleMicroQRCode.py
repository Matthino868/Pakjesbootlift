# import qrcode
# from PIL import Image

# # read in image file containing the QR code
# im = Image.open("C:/Users/arthu/Pictures/QRcodes/DeltaQR.png")

# # create a qr code reader object
# qr = qrcode.QRCode()

# # read the QR code from the image
# qr.scan_qr_code(im)

# # print the data contained in the QR code
# print(qr.get_data())




import cv2
from pyzbar.pyzbar import decode 

image = cv2.imread('C:/Users/arthu/Pictures/QRcodes/DeltaQR.png')

codes = decode(image)

print(codes)

microQR_codes = []
for code in codes:
    if code.type == "QRCODE" and code.data_type == "microQR":
        microQR_codes.append(code)

if microQR_codes:
    print("MicroQR codes detected:")
    for code in microQR_codes:
        print(code.data)
else:
    print("No microQR codes detected.")





# import qrcode
# from PIL import Image

# def recognize_microQR(image_file):
#     # read the image file and convert to grayscale
#     img = Image.open(image_file).convert('L')

#     # create a qrcode reader object
#     reader = qrcode.QRCode()

#     # read the qrcode from the image file
#     reader.scan(img)

#     # return the decoded data from the qrcode
#     return reader.data

# print(recognize_microQR('C:/Users/Melle/python/MircoQR.png'))


# import cv2
# import segno

# # Create a video capture object for the default camera
# cap = cv2.VideoCapture(0)

# while True:
#     # Capture a frame from the camera
#     _, frame = cap.read()

#     # Convert the frame to a grayscale image
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Decode the QR code in the image
#     result = segno.decode(gray)

#     if result:
#         # Get the decoded data
#         data = result[0].data.decode()

#         # Print the decoded data
#         print(data)

#     # Show the frame in a window
#     cv2.imshow('QR Code Decoder', frame)

#     # Break the loop when the user presses 'q'
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the video capture object
# cap.release()

# # Close all windows
# cv2.destroyAllWindows()
