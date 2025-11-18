import numpy as np
import cv2

canvas = np.zeros((300, 300, 3), dtype="uint8")

green = (0, 255, 0)
cv2.line(canvas, (0, 0), (300, 300), green)

red = (0, 0, 255)
cv2.line(canvas, (0, 300), (300, 0), red, 3)

blue = (255, 0, 0)
cv2.rectangle(canvas, (100, 100), (200, 200), blue, 1)


cv2.imshow("canvas", canvas)
cv2.waitKey(5000)
