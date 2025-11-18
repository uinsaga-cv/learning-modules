import numpy as np
import cv2

canvas = np.zeros((300, 300, 3), dtype="uint8")

# draw green
green = (0, 255, 0)
cv2.line(canvas, (0, 0), (300, 300), green)
cv2.imshow("Canvas", canvas)
cv2.waitKey(1000)

# draw red
red = (0, 0, 255)
# menggambar garis pada canvas (300x300), point awal (300,0), point akhir (0, 300), berwarna merah, dengan ketebalan 3px
cv2.line(canvas, (300, 0), (0, 300), red, 3)
cv2.imshow("Canvas", canvas)
cv2.waitKey(1000)

# draw rectangle
cv2.rectangle(canvas, (10, 10), (60, 60), green)
cv2.imshow("Canvas", canvas)
cv2.waitKey(1000)

cv2.rectangle(canvas, (50, 200), (200, 255), red, 5)
cv2.imshow("Canvas", canvas)
cv2.waitKey(1000)

blue = (255, 0, 0)
cv2.rectangle(canvas, (200, 50), (255, 125), blue, -1)
cv2.imshow("Canvas", canvas)
cv2.waitKey(0)
