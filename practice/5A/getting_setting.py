import os
import cv2

img_url = "./img/img-1.jpg"

path = os.path.join(".", img_url)
img = cv2.imread(path)


# pick a pixel from img
(b, g, r) = img[1500, 1250]
print("Pixel at (0, 0) - Red: {}, Green: {}, Blue: {}".format(r, g, b))

croped_image = img[1000:2000, 1000:2000]


cv2.imshow("ini gambarnya", croped_image)
cv2.waitKey(5000)
