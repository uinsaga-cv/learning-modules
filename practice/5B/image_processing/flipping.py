import numpy as np
import cv2
import os

# baca gambar
file_path = os.path.join(".", "./img/img-1.jpg")
image = cv2.imread(file_path)
flipped1 = cv2.flip(image, 1)
cv2.imshow("image", flipped1)
cv2.waitKey(5000)

flipped2 = cv2.flip(image, 0)
cv2.imshow("image", flipped2)
cv2.waitKey(5000)

flipped2 = cv2.flip(image, -1)
cv2.imshow("image", flipped2)
cv2.waitKey(5000)
