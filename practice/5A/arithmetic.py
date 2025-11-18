import cv2
import os
import numpy as np

# buka gambar dulu
img_path = os.path.join(".", "img/sample.png")
image = cv2.imread(img_path)

M = np.ones(image.shape, "uint8") * 100
added = cv2.add(image, M)


M = np.ones(image.shape, "uint8") * 50
subtract = cv2.subtract(image, M)

cv2.imshow("original", image)
cv2.imshow("contrast", added)
cv2.imshow("subs", subtract)
cv2.waitKey(5000)
