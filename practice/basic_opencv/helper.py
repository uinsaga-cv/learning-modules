import os
import cv2


def get_image(image_file: str):
    path = os.path.join(".", "img", image_file)
    return cv2.imread(path)


def show_image(image: cv2.Mat, name: str = "image", duration: int = None):
    cv2.imshow(name, image)
    cv2.setMouseCallback(name, show_pixel_position)
    if duration == None:
        cv2.waitKey(5000)
    else:
        cv2.waitKey(duration)


def wait(second: int = None):
    if second == None:
        cv2.waitKey(5000)
    else:
        cv2.waitKey(second * 1000)


def show_pixel_position(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # klik kiri
        print(f"Koordinat pixel: (x={x}, y={y})")
