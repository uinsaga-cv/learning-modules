import cv2
import os


pathImage = os.path.join(".", "sample.jpg")
image = cv2.imread(pathImage)

# to gray scala
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# to blurr
blurred = cv2.GaussianBlur(image, (5, 5), 0)
cv2.imshow("image ", image)

(T, tresh) = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)
cv2.imshow("tresh", tresh)

# # kebalikan binry inverse
# (T, threshInv) = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV)
# cv2.imshow("tresh inverse", threshInv)

# # pambarnya digabung
# bitand = cv2.bitwise_and(image, image, mask=threshInv)
# cv2.imshow("Coin", bitand)
cv2.waitKey(0)
