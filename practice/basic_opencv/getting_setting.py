import cv2
import os

path_image = os.path.join(".", "./img/img-1.jpg")
# load gambar
image = cv2.imread(path_image)
cv2.imshow("show image", image)
#  cv2.waitKey(0)


(b, g, r) = image[0, 0]
print("Pixel at (0, 0) - Red: {}, Green: {}, Blue: {}".format(r, g, b))

image[0, 0] = (0, 0, 255)
(b, g, r) = image[0, 0]
print("Pixel at (0, 0) - Red: {}, Green: {}, Blue: {}".format(r, g, b))

corner = image[0:100, 0:100]
cv2.imshow("Corner", corner)

image[0:2939, 0:2583] = (0, 255, 0)
cv2.imshow("Updated", image)
cv2.waitKey(0)
