import numpy as np
import cv2
import os

# baca gambar
file_path = os.path.join(".", "./img/img-1.jpg")
image = cv2.imread(file_path)


(height, width) = image.shape[:2]
center = (width // 2, height // 2)

# M = cv2.getRotationMatrix2D(center, 45, 1.0)
# retated = cv2.warpAffine(image, M, (width, height))
# cv2.imshow("shifted 45 derajat", retated)
# cv2.waitKey(5000)

# M = cv2.getRotationMatrix2D(center, 90, 1.0)
# retated = cv2.warpAffine(image, M, (width, height))
# cv2.imshow("shifted 45 derajat", retated)

for i in range(50):
    M = cv2.getRotationMatrix2D(center, i * -10, i * 0.02)
    retated = cv2.warpAffine(image, M, (width, height))
    cv2.imshow("shifted 45 derajat", retated)
    cv2.waitKey(1)
