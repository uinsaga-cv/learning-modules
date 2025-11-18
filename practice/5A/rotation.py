import cv2
import os
import numpy as np

# buka gambar dulu
img_path = os.path.join(".", "img/sample.png")
image = cv2.imread(img_path)

# (hight, width) = image.shape[:2]
hight = image.shape[0]
width = image.shape[1]
center = (width // 2, hight // 2)

for i in range(50):
    matrix = cv2.getRotationMatrix2D(center, 10 * i, i * 0.1)
    rotated = cv2.warpAffine(image, matrix, (width, hight))
    cv2.imshow("rotated", rotated)
    cv2.waitKey(500)
