import cv2
import numpy as np
import helper

image = helper.get_image("img-1.jpg")

mask = np.zeros(image.shape[:2], dtype="uint8")
(cX, cY) = (image.shape[1] // 2, image.shape[0] // 2)
cv2.rectangle(mask, (cX - 500, cY - 500), (cX + 500, cY + 500), 255, -1)
cv2.imshow("mask", mask)

masked = cv2.bitwise_and(image, image, mask=mask)
# helper.show_image(masked)

circleMask = np.zeros(image.shape[:2], dtype="uint8")
cv2.circle(circleMask, (cX, cY), 500, 255, -1)
circleMasked = cv2.bitwise_and(image, image, mask=circleMask)
helper.show_image(circleMasked)
