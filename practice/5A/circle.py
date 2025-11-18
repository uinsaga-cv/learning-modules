import numpy as np
import cv2


canvas = np.zeros((500, 500, 3), dtype="uint8")

titik_tengah = (250, 250)
radius = 50
biru = (255, 0, 0)
tebal = 3

cv2.circle(canvas, titik_tengah, radius, biru, tebal)

cv2.imshow("Lingkaran", canvas)
cv2.waitKey(5000)
