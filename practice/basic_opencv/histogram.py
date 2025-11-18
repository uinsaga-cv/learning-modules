import helper
import cv2
from matplotlib import pyplot as plt

image = helper.get_image("img-1.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

cv2.imshow("ori", image)
hist = cv2.calcHist([image], [0], None, [256], [0, 256])

plt.figure()
plt.title("Grayscale Histogram")
plt.xlabel("Bins")
plt.ylabel("# of Pixel")
plt.plot(hist)
plt.xlim([0, 256])
plt.show()
cv2.waitKey(5000)
