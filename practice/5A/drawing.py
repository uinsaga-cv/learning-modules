import cv2
import numpy as np


canvas = np.zeros((500, 500, 3), dtype="uint8")

cv2.line(canvas, (0, 0), (500, 500), (255, 255, 255), 3)
cv2.line(canvas, (0, 500), (500, 0), (0, 255, 0), 2)

cv2.rectangle(canvas, (200, 200), (300, 300), (0, 0, 255), -1)


cv2.imshow("canvas", canvas)
cv2.waitKey(5000)
