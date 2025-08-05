import cv2
import urllib.request
import numpy as np

# Load the pre-trained face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

url = 'http://192.168.29.248' cv2.namedWindow("gotcha", cv2.WINDOW_AUTOSIZE)

while True:
    try:
        # Fetch the image from the URL
        imgResponse = urllib.request.urlopen(url)
        imgnp = np.array(bytearray(imgResponse.read()), dtype=np.uint8)
        img = cv2.imdecode(imgnp, -1)

        # Convert the image to grayscale for face detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # Draw rectangles around the faces
        for (x, y, w, h) in faces:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)

        # Display the image
        cv2.imshow("gotcha", img)

        # Break the loop when 'q' is pressed
        key = cv2.waitKey(5)
        if key == ord('q'):
            break
    except Exception as e:
        print(f"Error: {e}")

cv2.destroyAllWindows()