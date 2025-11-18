import helper
import numpy as np
import cv2

rectangle = np.zeros((300, 300), dtype="uint8")
cv2.rectangle(rectangle, (25, 25), (275, 275), 255, -1)
cv2.imshow("rec", rectangle)

circle = np.zeros((300, 300), dtype="uint8")
cv2.circle(circle, (150, 150), 150, 255, -1)
cv2.imshow("cir", circle)

bitwiseAnd = cv2.bitwise_and(rectangle, circle)
helper.show_image(bitwiseAnd, "and", 2000)


bitwiseAnd = cv2.bitwise_or(rectangle, circle)
helper.show_image(bitwiseAnd, "or", 2000)


bitwiseAnd = cv2.bitwise_xor(rectangle, circle)
helper.show_image(bitwiseAnd, "xor", 2000)


bitwiseAnd = cv2.bitwise_not(rectangle, circle)
helper.show_image(bitwiseAnd, "not", 2000)
