import cv2
import numpy as np
import os

imgPath = os.path.join(".", "coin1.jpg")
img = cv2.imread(imgPath)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150)

contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for i, cnt in enumerate(contours):
    area = cv2.contourArea(cnt)
    if area > 100:
        cv2.drawContours(img, [cnt], -1, (0, 255, 0), 2)
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        x, y, w, h = cv2.boundingRect(approx)
        cv2.putText(
            img, f"Objek {i}", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2
        )

cv2.imshow("Contours", img)
cv2.waitKey(0)
