import cv2
import segno

# Create a video capture object for the default camera
cap = cv2.VideoCapture(0)

while True:
    # Capture a frame from the camera
    _, frame = cap.read()

    # Convert the frame to a grayscale image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Decode the QR code in the image
    result = segno.decode(gray)

    if result:
        # Get the decoded data
        data = result[0].data.decode()

        # Print the decoded data
        print(data)

    # Show the frame in a window
    cv2.imshow('QR Code Decoder', frame)

    # Break the loop when the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
cap.release()

# Close all windows
cv2.destroyAllWindows()
