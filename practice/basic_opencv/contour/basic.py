import cv2
import os

imgPath = os.path.join(".", "coin1.jpg")
img = cv2.imread(imgPath)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(
    thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)

cv2.drawContours(img, contours, -1, (0, 255, 0), 2)

cv2.imshow("Contours", img)
cv2.waitKey(0)
