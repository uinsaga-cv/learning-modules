import cv2
import os

imagePath = os.path.join(".", "sample.jpg")
image = cv2.imread(imagePath)

image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

blurred = cv2.GaussianBlur(image, (5, 5), 0)
# tresh = cv2.adaptiveThreshold(
#     blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 4
# )
# cv2.imshow("tresh mean", tresh)

treshG = cv2.adaptiveThreshold(
    blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 3
)
cv2.imshow("treshG", treshG)
cv2.waitKey(0)
