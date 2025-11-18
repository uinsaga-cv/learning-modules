import numpy as np
import cv2

canvas = np.zeros((500, 500, 3), dtype="uint8")

center_coordinate = (250, 50)
radius = 20
white = (255, 255, 255)
thickness = 3

# head
cv2.circle(canvas, center_coordinate, radius, white, thickness)
# body
cv2.line(canvas, (250, 70), (250, 170), white, thickness)
# hand
cv2.line(canvas, (200, 85), (300, 85), white, thickness)
# left foot
cv2.line(canvas, (250, 170), (200, 220), white, thickness)
# right foot
cv2.line(canvas, (250, 170), (300, 220), white, thickness)
cv2.imshow("Canvas", canvas)
cv2.waitKey(0)

# for i in range(10):
#     cv2.circle(canvas, center_coordinate, radius, (0, 0, 0), thickness)
#     cv2.imshow("Canvas", canvas)
#     cv2.waitKey(100)

#     cv2.circle(canvas, center_coordinate, radius, white, thickness)
#     cv2.imshow("Canvas", canvas)
#     cv2.waitKey(100)
