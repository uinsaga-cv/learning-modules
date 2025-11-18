import numpy as np
import cv2

canvas = np.zeros((500, 500, 3), np.uint8)

center_coordinate = (250, 50)
radius = 20
color = (0, 255, 0)
thickness = 3

cv2.circle(canvas, center_coordinate, radius, color, thickness)

# line
cv2.line(canvas, (250, 70), (250, 120), color, thickness)
cv2.line(canvas, (90, 90), (300, 90), color, thickness)
cv2.line(canvas, (250, 120), (220, 170), color, thickness)
cv2.line(canvas, (250, 120), (270, 170), color, thickness)
cv2.imshow("Canvas", canvas)
cv2.waitKey(100)

# line
cv2.line(canvas, (90, 90), (300, 90), (0, 0, 0), thickness)
cv2.line(canvas, (90, 120), (300, 90), color, thickness)
cv2.imshow("Canvas", canvas)
cv2.waitKey(100)

cv2.line(canvas, (90, 120), (300, 90), (0, 0, 0), thickness)
cv2.line(canvas, (90, 70), (300, 90), color, thickness)
cv2.imshow("Canvas", canvas)
cv2.waitKey(100)

for i in range(10):
    cv2.line(canvas, (90, 70), (300, 90), (0, 0, 0), thickness)
    cv2.line(canvas, (90, 90), (300, 90), color, thickness)
    cv2.imshow("Canvas", canvas)
    cv2.waitKey(100)

    # line
    cv2.line(canvas, (90, 90), (300, 90), (0, 0, 0), thickness)
    cv2.line(canvas, (90, 120), (300, 90), color, thickness)
    cv2.imshow("Canvas", canvas)
    cv2.waitKey(100)

    cv2.line(canvas, (90, 120), (300, 90), (0, 0, 0), thickness)
    cv2.line(canvas, (90, 70), (300, 90), color, thickness)
    cv2.imshow("Canvas", canvas)
    cv2.waitKey(100)
