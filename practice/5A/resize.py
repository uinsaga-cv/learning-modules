import cv2
import os
import numpy as np

# buka gambar dulu
img_path = os.path.join(".", "img/sample.png")
image = cv2.imread(img_path)

# (hight, width) = image.shape[:2]
hight = image.shape[0]
width = image.shape[1]

target_resize = 200
ratio = target_resize / width
dim = (target_resize, int(hight * ratio))

resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

flipped = cv2.flip(resized, 1)
cv2.imshow("resized", resized)
cv2.imshow("flipped", flipped)

cropped = flipped[50:100, 50:100]
cv2.imshow("cropped", cropped)

cv2.waitKey(5000)
