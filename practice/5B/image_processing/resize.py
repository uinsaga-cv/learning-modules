import numpy as np
import cv2
import os

# baca gambar
file_path = os.path.join(".", "./img/img-1.jpg")
image = cv2.imread(file_path)

resize = 150 / (image.shape[1])
dimension = (150, int(image.shape[0] * resize))

resized = cv2.resize(image, dimension, interpolation=cv2.INTER_AREA)

cv2.imshow("resized", resized)
cv2.waitKey(5000)
