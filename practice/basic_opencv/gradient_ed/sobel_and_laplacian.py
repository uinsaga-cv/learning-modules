import cv2
import numpy as np
import os


imagePath = os.path.join(".", "coin1.jpg")
image = cv2.imread(imagePath)
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

lap = cv2.Laplacian(image, cv2.CV_64F)
lap = np.uint8(np.absolute(lap))
cv2.imshow("lap", lap)
cv2.waitKey(10000)
