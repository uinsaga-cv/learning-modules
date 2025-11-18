# Contour Lanjut

## 1. Pengantar

**Contour (kontur)** adalah garis lengkung yang menghubungkan titik-titik dengan intensitas sama dalam citra.
Kontur digunakan untuk mendeteksi dan menganalisis bentuk objek, seperti menghitung luas, keliling, mendeteksi bentuk, atau melacak objek.

Dalam OpenCV, kontur biasanya ditemukan dari citra **biner** hasil proses thresholding atau edge detection (misalnya Canny).

---

## 2. Konsep Dasar

Langkah umum dalam mendeteksi kontur:

1. Konversi gambar ke grayscale
2. Lakukan thresholding atau edge detection
3. Temukan kontur dengan `cv2.findContours()`
4. Gambar kontur dengan `cv2.drawContours()`

Fungsi:

```python
contours, hierarchy = cv2.findContours(image, mode, method)
```

Parameter:

* `image`: citra biner (0 dan 255)
* `mode`: menentukan level kontur yang dicari (misalnya `cv2.RETR_EXTERNAL`, `cv2.RETR_TREE`)
* `method`: cara menyimpan titik kontur (misalnya `cv2.CHAIN_APPROX_SIMPLE`)

---

## 3. Contoh Dasar

```python
import cv2

img = cv2.imread('object.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(img, contours, -1, (0, 255, 0), 2)

cv2.imshow('Contours', img)
cv2.waitKey(0)
```

---

## 4. Menghitung Luas dan Keliling

```python
cnt = contours[0]
area = cv2.contourArea(cnt)
perimeter = cv2.arcLength(cnt, True)
```

`cv2.contourArea()` menghitung luas kontur,
`cv2.arcLength()` menghitung keliling kontur.

---

## 5. Bentuk Pembatas (Bounding Shapes)

a. **Bounding Rectangle**

```python
x, y, w, h = cv2.boundingRect(cnt)
cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
```

b. **Minimum Enclosing Circle**

```python
(x, y), radius = cv2.minEnclosingCircle(cnt)
cv2.circle(img, (int(x), int(y)), int(radius), (0, 255, 255), 2)
```

c. **Convex Hull**

```python
hull = cv2.convexHull(cnt)
cv2.drawContours(img, [hull], 0, (0, 0, 255), 2)
```

---

## 6. Approximation (Penyederhanaan Kontur)

Untuk menyederhanakan bentuk kontur tanpa kehilangan karakteristik bentuk utama:

```python
epsilon = 0.02 * cv2.arcLength(cnt, True)
approx = cv2.approxPolyDP(cnt, epsilon, True)
cv2.drawContours(img, [approx], 0, (255, 0, 255), 3)
```

Jika hasil approximation memiliki 3 titik berarti segitiga,
4 titik berarti persegi, dan lebih dari 4 berarti bentuk poligon.

---

## 7. Hierarchy Kontur

Hierarchy berisi hubungan antar kontur:

* Kontur di dalam kontur (nested objects)
* Anak, induk, atau kontur sejajar

Struktur `hierarchy`:

```
[[[next, previous, first_child, parent]]]
```

Gunakan `cv2.RETR_TREE` untuk mendapatkan seluruh struktur hierarki.

---

## 8. Contoh Lengkap

```python
import cv2
import numpy as np

img = cv2.imread('shapes.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150)

contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for i, cnt in enumerate(contours):
    area = cv2.contourArea(cnt)
    if area > 100:
        cv2.drawContours(img, [cnt], -1, (0, 255, 0), 2)
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        x, y, w, h = cv2.boundingRect(approx)
        cv2.putText(img, f"Objek {i}", (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)

cv2.imshow('Contours', img)
cv2.waitKey(0)
```

---

## 9. Contour Moments

Moments menggambarkan bentuk dan distribusi piksel pada kontur.
OpenCV menyediakan fungsi:

```python
M = cv2.moments(cnt)
```

Centroid (pusat massa) dihitung dengan:

```
cx = M["m10"] / M["m00"]
cy = M["m01"] / M["m00"]
```

Contoh:

```python
M = cv2.moments(cnt)
cx = int(M["m10"]/M["m00"])
cy = int(M["m01"]/M["m00"])
cv2.circle(img, (cx, cy), 5, (0,0,255), -1)
```

---

## 10. Shape Matching

Untuk membandingkan dua bentuk kontur:

```python
similarity = cv2.matchShapes(cnt1, cnt2, cv2.CONTOURS_MATCH_I1, 0.0)
```

Nilai semakin kecil berarti bentuk semakin mirip.

---

## 11. Convexity Defects

Convexity defects menunjukkan lekukan antara kontur dan convex hull-nya.

```python
hull = cv2.convexHull(cnt, returnPoints=False)
defects = cv2.convexityDefects(cnt, hull)
for i in range(defects.shape[0]):
    s, e, f, d = defects[i, 0]
    start = tuple(cnt[s][0])
    end = tuple(cnt[e][0])
    far = tuple(cnt[f][0])
    cv2.line(img, start, end, (0, 255, 0), 2)
    cv2.circle(img, far, 5, (0, 0, 255), -1)
```

Fitur ini berguna untuk analisis gesture atau deteksi jari.

---

## 12. Orientasi Kontur

Menggunakan `cv2.fitEllipse()` untuk mendapatkan orientasi dan bentuk elips:

```python
ellipse = cv2.fitEllipse(cnt)
cv2.ellipse(img, ellipse, (255, 0, 0), 2)
```

Fungsi ini menghasilkan pusat, sumbu mayor & minor, dan sudut kemiringan objek.

---

## 13. Sorting Kontur

Urutkan kontur berdasarkan area:

```python
sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
```

Urutkan berdasarkan posisi X (kiri ke kanan):

```python
def sort_by_x(cnt):
    x, y, w, h = cv2.boundingRect(cnt)
    return x

sorted_contours = sorted(contours, key=sort_by_x)
```

---

## 14. Rangkuman Fungsi

| Fungsi                     | Keterangan                             |
| -------------------------- | -------------------------------------- |
| `cv2.findContours()`       | Menemukan kontur dari citra biner      |
| `cv2.drawContours()`       | Menggambar kontur pada citra           |
| `cv2.contourArea()`        | Menghitung luas kontur                 |
| `cv2.arcLength()`          | Menghitung keliling kontur             |
| `cv2.boundingRect()`       | Menentukan kotak pembatas              |
| `cv2.minEnclosingCircle()` | Menentukan lingkaran pembatas          |
| `cv2.convexHull()`         | Membentuk area konveks                 |
| `cv2.approxPolyDP()`       | Menyederhanakan bentuk kontur          |
| `cv2.moments()`            | Menghitung pusat massa dan momen       |
| `cv2.matchShapes()`        | Membandingkan kemiripan bentuk         |
| `cv2.convexityDefects()`   | Menemukan lekukan pada kontur          |
| `cv2.fitEllipse()`         | Menentukan orientasi elips dari kontur |

---

## 15. Kesimpulan

* Kontur digunakan untuk mendeteksi dan menganalisis bentuk objek.
* Untuk menemukan kontur, gambar harus diubah menjadi biner terlebih dahulu.
* Fitur lanjutan seperti moments, convexity defects, dan shape matching sangat berguna dalam analisis bentuk dan pengenalan objek.
* Kombinasi kontur dengan edge detection atau thresholding memberikan hasil yang lebih stabil dan akurat.

---

## 16. Referensi

* OpenCV Documentation: [https://docs.opencv.org](https://docs.opencv.org)
* Gonzalez & Woods, *Digital Image Processing* (4th Edition)
* PyImageSearch: “Shape Detection and Contour Analysis with OpenCV”
