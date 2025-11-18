import helper
import cv2


image = helper.get_image("img-1.jpg")

grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("grey", grey)
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
cv2.imshow("hsv", hsv)
lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
cv2.imshow("lab", lab)

helper.wait(5)
