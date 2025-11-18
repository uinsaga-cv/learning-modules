import os
import cv2 as cv

# open file
imagePath = os.path.join("./img", "img-1.jpg")
# membaca gambar
image = cv.imread(imagePath)

# menampilkan gambar
cv.imshow("gambarnya", image)

# digunakan untuk
cv.waitKey(10000)

cv.destroyAllWindows()
