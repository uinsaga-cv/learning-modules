# Gradient and Edge Detection in OpenCV

## 1. Pengantar

**Edge detection (deteksi tepi)** adalah proses menemukan perubahan intensitas yang signifikan di dalam citra.  
Tepi biasanya menunjukkan batas antara dua area dengan perbedaan intensitas yang kuat — seperti batas objek.

Edge penting dalam:

- Segmentasi objek
- Pengenalan bentuk
- Deteksi fitur (feature extraction)

---

## 2. Konsep Dasar Gradient

**Gradient** mengukur perubahan intensitas (brightness) antar piksel di arah tertentu.  
Secara matematis, gradient adalah **turunan (derivative)** dari citra terhadap sumbu X dan Y.

```math
[
\text{Gradient Magnitude: } G = \sqrt{G_x^2 + G_y^2}
]
```
```math
[
\text{Gradient Direction: } \theta = \tan^{-1}\left(\frac{G_y}{G_x}\right)
]
```

di mana:

```bash
- \( G_x \): turunan terhadap sumbu X  
- \( G_y \): turunan terhadap sumbu Y
```

Tepi muncul di lokasi dengan **perubahan intensitas tajam**, yaitu di mana nilai gradient besar.

---

## 3. Laplacian Operator

### Teori

**Laplacian** menghitung *second derivative* (turunan kedua) dari citra, yaitu:
\[
\nabla^2 f = \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2}
\]

Operator ini mendeteksi area dengan perubahan intensitas cepat ke dua arah (positif dan negatif).  
Karena itu, hasilnya bisa menunjukkan tepi sebagai nilai positif atau negatif di sekitar batas objek.

### Contoh Kode

```python
import cv2
import numpy as np

img = cv2.imread('image.jpg', 0)
laplacian = cv2.Laplacian(img, cv2.CV_64F)
laplacian = np.uint8(np.absolute(laplacian))

cv2.imshow('Laplacian Edge', laplacian)
cv2.waitKey(0)
```

### Catatan

* `cv2.CV_64F` digunakan untuk menjaga nilai negatif dari turunan kedua.
* Hasil biasanya diubah ke nilai absolut agar tampil baik saat divisualisasi.

---

## 4. Sobel Operator

### 📘 Teori

**Sobel operator** menghitung turunan pertama citra secara terpisah di arah X dan Y.
Ia menggabungkan operasi **Gaussian smoothing** dan **differentiation** untuk mengurangi noise.

Kernel Sobel:

```math
[
G_x =
\begin{bmatrix}
-1 & 0 & 1\
-2 & 0 & 2\
-1 & 0 & 1
\end{bmatrix}
,\quad
G_y =
\begin{bmatrix}
-1 & -2 & -1\
0 & 0 & 0\
1 & 2 & 1
\end{bmatrix}
]
```

### 💻 Contoh Kode

```python
import cv2
import numpy as np

img = cv2.imread('image.jpg', 0)

# Sobel di arah X dan Y
sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)

# Gabungkan magnitude
sobel_combined = cv2.magnitude(sobelx, sobely)
sobel_combined = np.uint8(np.absolute(sobel_combined))

cv2.imshow('Sobel X', np.uint8(np.absolute(sobelx)))
cv2.imshow('Sobel Y', np.uint8(np.absolute(sobely)))
cv2.imshow('Sobel Combined', sobel_combined)
cv2.waitKey(0)
```

### Catatan

* Parameter `ksize` menentukan ukuran kernel (biasanya 3).
* Sobel lebih halus daripada Prewitt karena memiliki efek smoothing (mengurangi noise).

---

## 5. Canny Edge Detector

### Teori

**Canny Edge Detector** (John F. Canny, 1986) merupakan algoritma deteksi tepi yang **multi-tahap** dan sangat efektif karena mempertimbangkan *noise reduction*, *gradient magnitude*, serta *edge linking*.

Tahapan algoritma:

1. **Noise Reduction**
   Gunakan Gaussian blur untuk menghaluskan citra.

   ```math
   [
   I_{smooth} = I * G
   ]
   ```

2. **Compute Gradient Magnitude dan Direction**
   Hitung turunan ( G_x, G_y ) → lalu magnitude ( M = \sqrt{G_x^2 + G_y^2} ).

3. **Non-Maximum Suppression**
   Hanya pertahankan piksel yang merupakan puncak (lokal maksimum) dalam arah gradient.

4. **Double Thresholding**
   Gunakan dua nilai threshold: `low` dan `high` untuk klasifikasi:

   * Piksel > high → *strong edge*
   * Piksel antara low–high → *weak edge*
   * Piksel < low → *non-edge*

5. **Edge Tracking by Hysteresis**
   Weak edge yang terhubung ke strong edge akan tetap dipertahankan.

### Contoh Kode

```python
import cv2

img = cv2.imread('image.jpg', 0)
blur = cv2.GaussianBlur(img, (5,5), 1.4)
edges = cv2.Canny(blur, 100, 200)

cv2.imshow('Canny Edge', edges)
cv2.waitKey(0)
```

### 🔍 Catatan

* Parameter `(100, 200)` adalah `low_threshold` dan `high_threshold`.
* Atur nilai ini sesuai kontras gambar.
* Canny sangat baik untuk mendeteksi tepi halus namun jelas.

---

## 6. Perbandingan Metode

| Metode        | Prinsip                                          | Kelebihan                        | Kekurangan                      |
| ------------- | ------------------------------------------------ | -------------------------------- | ------------------------------- |
| **Laplacian** | Turunan kedua (2D)                               | Sederhana, deteksi semua arah    | Sensitif terhadap noise         |
| **Sobel**     | Turunan pertama (X, Y)                           | Stabil, mengandung smoothing     | Kurang akurat di area kabur     |
| **Canny**     | Multi-tahap (derivative + filtering + threshold) | Akurasi tinggi, noise resistance | Lebih kompleks, butuh parameter |

---

## 7. Contoh Gabungan Visualisasi

```python
import cv2
import numpy as np

img = cv2.imread('image.jpg', 0)
blur = cv2.GaussianBlur(img, (5,5), 1)

# Laplacian
lap = cv2.Laplacian(img, cv2.CV_64F)
lap = np.uint8(np.absolute(lap))

# Sobel
sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
sobel = cv2.magnitude(sobelx, sobely)
sobel = np.uint8(np.absolute(sobel))

# Canny
canny = cv2.Canny(blur, 100, 200)

cv2.imshow('Original', img)
cv2.imshow('Laplacian', lap)
cv2.imshow('Sobel', sobel)
cv2.imshow('Canny', canny)
cv2.waitKey(0)
```

---

## 8. Tips Praktik

* Selalu lakukan **Gaussian blur** sebelum deteksi tepi untuk mengurangi noise.
* Gunakan `cv2.CV_64F` untuk menghindari kehilangan informasi negatif pada turunan.
* Sesuaikan threshold pada Canny agar tidak terlalu banyak atau terlalu sedikit tepi.
* Untuk visualisasi hasil, gunakan kombinasi `cv2.imshow()` atau `matplotlib.pyplot`.

---

## 9. Referensi

* J. F. Canny, *“A Computational Approach to Edge Detection”*, IEEE Trans. PAMI, 1986.
* Gonzalez & Woods, *Digital Image Processing*, 4th Ed.
* OpenCV Documentation: [https://docs.opencv.org](https://docs.opencv.org)

---