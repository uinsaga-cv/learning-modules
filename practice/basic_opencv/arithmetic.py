import helper
import numpy as np
import cv2

image = helper.get_image("sample.png")

M = np.ones(image.shape, dtype="uint8") * 100
added = cv2.add(image, M)
helper.show_image(added)

M = np.ones(image.shape, dtype="uint8") * 50
substracted = cv2.subtract(image, M)
helper.show_image(substracted)
