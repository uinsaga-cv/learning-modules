# Thresholding

## 🧠 **1. Pengertian Thresholding (Teori Dasar)**

Thresholding adalah teknik segmentasi citra yang memisahkan **objek (foreground)** dari **latar belakang (background)** dengan menetapkan nilai ambang (threshold) tertentu.

Setiap piksel akan dibandingkan dengan nilai ambang:

* Jika nilai piksel > threshold → diklasifikasikan sebagai **objek** (biasanya putih, 255)
* Jika nilai piksel ≤ threshold → diklasifikasikan sebagai **latar belakang** (hitam, 0)

Hasil akhirnya adalah **citra biner (binary image)**.

---

## **2. Jenis Thresholding**

### **A. Simple (Global) Thresholding**

#### Teori

Nilai threshold **T** ditentukan secara tetap untuk seluruh citra.
Biasanya dipilih berdasarkan percobaan (misal T = 127).

Rumusnya:
```math
[
g(x,y) =
\begin{cases}
1, & \text{jika } f(x,y) > T \
0, & \text{jika } f(x,y) \leq T
\end{cases}
]
```

di mana:

```bash
* ( f(x,y) ): intensitas piksel input
* ( g(x,y) ): hasil biner (0 atau 1)
```

#### 📋 Algoritma

1. Konversi gambar ke grayscale.
2. Tentukan nilai ambang ( T ).
3. Bandingkan setiap piksel terhadap ( T ).
4. Ganti nilainya menjadi 0 atau 255.

#### 💻 Contoh kode

```python
import cv2

img = cv2.imread('image.jpg', 0)
ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
```

---

### **B. Adaptive Thresholding**

#### Teori

Digunakan ketika pencahayaan tidak merata di seluruh citra.
Alih-alih satu nilai ambang global, setiap piksel memiliki threshold **lokal** yang dihitung berdasarkan tetangganya.

Terdapat dua metode:

1. **Mean adaptive** → threshold = rata-rata nilai tetangga − C
2. **Gaussian adaptive** → threshold = bobot Gaussian dari tetangga − C

#### 📋 Algoritma

1. Bagi citra menjadi blok-blok kecil (misal 11×11).
2. Hitung rata-rata atau Gaussian weighted sum dari setiap blok.
3. Kurangi dengan konstanta ( C ).
4. Bandingkan nilai piksel dengan threshold lokal.

#### 💻 Contoh kode

```python
thresh_mean = cv2.adaptiveThreshold(
    img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
    cv2.THRESH_BINARY, 11, 2)

thresh_gauss = cv2.adaptiveThreshold(
    img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY, 11, 2)
```

---

### 🟥 **C. Otsu’s Thresholding**

#### 📘 Teori

Otsu (1979) mengusulkan metode untuk menghitung nilai ambang **otomatis** berdasarkan **distribusi histogram** citra.

Ia berasumsi citra terdiri dari dua kelas (foreground dan background) dan mencari nilai ( T ) yang **meminimalkan variansi intra-kelas** atau **memaksimalkan variansi antar-kelas**.

Rumus matematis:

```math
[
\sigma_b^2(T) = \omega_0(T)\omega_1(T)[\mu_0(T) - \mu_1(T)]^2
]
```

Otsu mencari nilai ( T ) yang **memaksimalkan** ( \sigma_b^2(T) ).


#### 📋 Algoritma Otsu

1. Hitung histogram dan probabilitas setiap intensitas.
2. Untuk setiap nilai threshold ( T ):

   * Hitung bobot kelas ( \omega_0, \omega_1 )
   * Hitung rata-rata kelas ( \mu_0, \mu_1 )
   * Hitung variansi antar kelas ( \sigma_b^2(T) )
3. Pilih ( T ) dengan ( \sigma_b^2 ) maksimum.

#### Contoh kode

```python
import cv2

img = cv2.imread('image.jpg', 0)
blur = cv2.GaussianBlur(img, (5,5), 0)
ret, otsu = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
print("Nilai threshold Otsu:", ret)
```

---

### **D. Ridler–Calvard (Iterative Thresholding)**

#### Teori

Disebut juga **Iterative Selection Method**, dikembangkan oleh Ridler dan Calvard (1978).
Pendekatannya adalah iteratif: dimulai dengan perkiraan awal, lalu diperbarui hingga konvergen.

#### 📋 Algoritma Ridler-Calvard

1. Hitung rata-rata intensitas seluruh piksel → ( T_0 ).
2. Bagi citra menjadi dua grup:

   * ( G_1 ): piksel > ( T )
   * ( G_2 ): piksel ≤ ( T )
3. Hitung rata-rata masing-masing grup ( \mu_1, \mu_2 ).
4. Hitung threshold baru:
  
  ```math
   [
   T_{baru} = \frac{\mu_1 + \mu_2}{2}
   ]
   ```

5. Ulangi langkah 2–4 sampai ( |T_{baru} - T_{lama}| < \epsilon ) (konvergen).

#### 💻 Contoh kode (Python)

```python
import cv2
import numpy as np

def ridler_calvard_threshold(image, epsilon=0.5):
    T = np.mean(image)
    while True:
        G1 = image[image > T]
        G2 = image[image <= T]
        T_new = (np.mean(G1) + np.mean(G2)) / 2
        if abs(T - T_new) < epsilon:
            break
        T = T_new
    return T

img = cv2.imread('image.jpg', 0)
T_rc = ridler_calvard_threshold(img)
_, thresh_rc = cv2.threshold(img, T_rc, 255, cv2.THRESH_BINARY)
print("Threshold Ridler-Calvard:", T_rc)
```

---

## ⚖️ **3. Perbandingan Umum**

| Metode         | Prinsip               | Kelebihan                                | Kekurangan                                 |
| -------------- | --------------------- | ---------------------------------------- | ------------------------------------------ |
| Simple         | Ambang tetap global   | Cepat, mudah                             | Tidak cocok untuk pencahayaan tidak merata |
| Adaptive       | Ambang lokal per blok | Baik untuk cahaya tidak merata           | Lebih lambat, perlu parameter              |
| Otsu           | Statistik histogram   | Otomatis, tanpa parameter manual         | Kurang efektif untuk multi-objek           |
| Ridler–Calvard | Iteratif rata-rata    | Lebih stabil dari Otsu di beberapa kasus | Butuh iterasi, lebih lama                  |
