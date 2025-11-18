import numpy as np
import cv2
import os

# baca gambar
file_path = os.path.join(".", "./img/img-1.jpg")

image = cv2.imread(file_path)
cropped = image[30:120, 240:335]

cv2.imshow("cropped", cropped)
cv2.waitKey(5000)
