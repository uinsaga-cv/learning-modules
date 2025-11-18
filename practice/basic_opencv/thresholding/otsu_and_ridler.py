# OTSU AND RIDDLER CALVARD

import cv2
import mahotas
import os


imagePath = os.path.join(".", "sample.jpg")
img = cv2.imread(imagePath)
image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(image, (5, 5), 0)
cv2.imshow("blurred", blurred)

T = mahotas.thresholding.otsu(blurred)

thresh = image.copy()
thresh[thresh > T] = 255
thresh = cv2.bitwise_not(thresh)
cv2.imshow("otsu", thresh)

T = mahotas.thresholding.rc(blurred)
thresh = image.copy()
thresh[thresh > T] = 255
thresh[thresh < 255] = 0
thresh = cv2.bitwise_not(thresh)
cv2.imshow("riddler calvard", thresh)


cv2.waitKey(0)
