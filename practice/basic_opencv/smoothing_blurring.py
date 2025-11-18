import helper
import cv2
import numpy as np


image = helper.get_image("img-1.jpg")

# averaging
# blurred = np.hstack(
#     [
#         cv2.blur(image, (10, 10)),
#         cv2.blur(image, (50, 50)),
#         cv2.blur(image, (70, 70)),
#     ]
# )
# helper.show_image(blurred)


# GaussianBlur
# gBlurred = np.hstack(
#     [
#         cv2.GaussianBlur(image, (3, 3), 0),
#         cv2.GaussianBlur(image, (5, 5), 0),
#         cv2.GaussianBlur(image, (7, 7), 0),
#     ]
# )
# helper.show_image(gBlurred)

# Median
# gBlurred = np.hstack(
#     [
#         cv2.medianBlur(
#             image,
#             3,
#         ),
#         cv2.medianBlur(
#             image,
#             5,
#         ),
#         cv2.medianBlur(
#             image,
#             7,
#         ),
#     ]
# )
# helper.show_image(gBlurred)

bBlurred = np.hstack(
    [
        cv2.bilateralFilter(image, 5, 21, 21),
        cv2.bilateralFilter(image, 5, 21, 31),
        cv2.bilateralFilter(image, 5, 21, 41),
    ]
)
helper.show_image(bBlurred)
