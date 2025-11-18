import cv2
import os

imagepath = os.path.join(".", "coin1.jpg")
img = cv2.imread(imagepath, 0)
blur = cv2.GaussianBlur(img, (5, 5), 1.4)
edges = cv2.Canny(blur, 100, 200)

cv2.imshow("Canny Edge", edges)
cv2.waitKey(0)
