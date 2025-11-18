import cv2
import os

xmlPath = os.path.join(".", "assets/xml", "haarcascade_frontalface_default.xml")
face_cascade = cv2.CascadeClassifier(xmlPath)

imgPath = os.path.join(".", "img", "children.jpg")
image = cv2.imread(imgPath)

imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(imageGray, scaleFactor=1.1, minNeighbors=5)

for x, y, w, h in faces:
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 5)

cv2.imshow("children", image)
cv2.waitKey(0)
