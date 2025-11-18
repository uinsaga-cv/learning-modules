import helper
import cv2
from matplotlib import pyplot as plt

image = helper.get_image("img-1.jpg")
cv2.imshow("ori", image)

chans = cv2.split(image)
colors = ("b", "g", "r")

plt.figure()
plt.title("Flattened color Histogram")
plt.xlabel("Bins")
plt.ylabel("# of Pixel")

for chan, color in zip(chans, colors):
    hist = cv2.calcHist([chan], [0], None, [256], [0, 255])
    plt.plot(hist, color=color)
    plt.xlim([0, 256])

plt.show()
cv2.waitKey(5000)
