import numpy as np
import cv2
import os
import argparse


def translate(image, lr, td):
    Matrix = np.float32([[1, 0, lr], [0, 1, td]])
    return cv2.warpAffine(image, Matrix, (image.shape[1], image.shape[0]))


# image_path = os.path.join(".", "img-1.jpg")

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())


image = cv2.imread(args["image"])

shifted = translate(image, -300, 300)

cv2.imshow("image", shifted)
cv2.waitKey(5000)
