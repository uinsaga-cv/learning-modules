import numpy as np
import cv2
import os

# baca gambar
file_path = os.path.join(".", "./img/img-1.jpg")
image = cv2.imread(file_path)

sMatrix = np.float32([[1, 0, 250], [0, 1, 500]])
shifted = cv2.warpAffine(image, sMatrix, [image.shape[1], image.shape[0]])


cv2.imshow("shifted", shifted)
cv2.waitKey(5000)
