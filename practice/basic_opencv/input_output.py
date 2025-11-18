import os
import cv2

# open file dan menampilkannya
img_path = os.path.join("./img", "img-1.jpg")
source_image = cv2.imread(img_path)
cv2.imshow("gambar awal", source_image)

# buat image dari sumber ke nama output
output_image = os.path.join("./img", "output.jpg")
success = cv2.imwrite(output_image, source_image)

if success:
    print(f"Image '{output_image}' saved successfully.")
    # manmpilkan hasil gambar
    result = cv2.imread(output_image)
    cv2.imshow("gambar hasil", result)

else:
    print(f"Failed to save image '{output_image}'.")

cv2.waitKey(10000)
cv2.destroyAllWindows()
