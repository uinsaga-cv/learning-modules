import cv2
import os
import numpy as np

# buka gambar dulu
img_path = os.path.join(".", "img/sample.png")
image = cv2.imread(img_path)

cv2.imshow("subs", subtract)
cv2.waitKey(5000)
