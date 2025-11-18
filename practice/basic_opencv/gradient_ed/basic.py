import cv2
import os
import numpy as np

imagepath = os.path.join(".", "coin1.jpg")
img = cv2.imread(imagepath, 0)
laplacian = cv2.Laplacian(img, cv2.CV_64F)
laplacian = np.uint8(np.absolute(laplacian))

cv2.imshow("Canny Edge", laplacian)
cv2.waitKey(0)
