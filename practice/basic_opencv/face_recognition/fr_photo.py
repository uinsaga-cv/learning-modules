import cv2
import json

# load model + label
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("assets/face_model.xml")

with open("assets/labels.json", "r") as f:
    label_ids = json.load(f)

face_cascade = cv2.CascadeClassifier("assets/haarcascade_frontalface_default.xml")

img = cv2.imread("aj.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, 1.3, 5)

for x, y, w, h in faces:
    face_roi = gray[y : y + h, x : x + w]
    label, confidence = recognizer.predict(face_roi)

    name = label_ids[str(label)]
    text = f"{name} ({confidence:.1f})"

    cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

cv2.imshow("Result", img)
cv2.waitKey(5000)
