import cv2
import numpy as np
import os

imagePath = os.path.join(".", "coin1.jpg")
img = cv2.imread(imagePath)

# Sobel di arah X dan Y
sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)

# Gabungkan magnitude
sobel_combined = cv2.magnitude(sobelx, sobely)
sobel_combined = np.uint8(np.absolute(sobel_combined))

cv2.imshow("Sobel X", np.uint8(np.absolute(sobelx)))
cv2.imshow("Sobel Y", np.uint8(np.absolute(sobely)))
cv2.imshow("Sobel Combined", sobel_combined)
cv2.waitKey(0)
