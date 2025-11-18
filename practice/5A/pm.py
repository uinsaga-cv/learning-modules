import numpy as np
import cv2

canvas = np.zeros((500, 500, 3), dtype="uint8")

(centerx, centery) = (canvas.shape[1] // 2, canvas.shape[0] // 2)

body_radius = 100
body_center = (centerx, centery)

cv2.circle(canvas, body_center, body_radius, (0, 255, 255), -1)

mouth = np.array(
    [
        [centerx, centery],
        [centerx + 100, centery - 50],
        [centerx + 100, centery + 50],
    ],
    np.int32,
)

cv2.fillPoly(canvas, [mouth], (0, 0, 0))

cv2.imshow("Pacman", canvas)
cv2.waitKey(5000)
