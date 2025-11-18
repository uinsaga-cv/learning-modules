import cv2
import os
import numpy as np
import argparse


def translation(image, x, y):
    afin_matrix = np.float32([[1, 0, x], [0, 1, y]])
    return cv2.warpAffine(image, afin_matrix, (image.shape[1], image.shape[0]))


# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True, help="Path to the image")
# ap.add_argument("-t", "--translate", required=True, help="translate")
# args = vars(ap.parse_args())

img_path = os.path.join(".", "img/sample.png")
image = cv2.imread(img_path)
geser = translation(image, -100, 100)
cv2.imshow("image", geser)
cv2.imwrite("tranlated.png", geser)
cv2.waitKey(5000)
