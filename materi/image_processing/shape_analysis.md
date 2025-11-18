# **Shape Analysis & Object Measurement menggunakan Contour di OpenCV**

---

## 1. Pengantar

Setelah memahami dasar **deteksi kontur**, tahap berikutnya adalah **analisis bentuk (shape analysis)** dan **pengukuran objek (object measurement)**.
Tujuan utamanya adalah mengekstrak informasi **geometris** dari objek seperti:

* Luas dan keliling
* Titik pusat (centroid)
* Dimensi panjang dan lebar
* Radius (jika berbentuk lingkaran)
* Orientasi (arah rotasi)
* Perbandingan bentuk (shape similarity)

---

## 2. Persiapan Dasar

Proses pengukuran dimulai dengan segmentasi objek agar kontur dapat diambil secara bersih.

```python
import cv2
import numpy as np

img = cv2.imread('objects.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
ret, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```

---

## 3. Menghitung Luas, Keliling, dan Pusat

```python
for cnt in contours:
    area = cv2.contourArea(cnt)
    perimeter = cv2.arcLength(cnt, True)
    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    
    cv2.circle(img, (cx, cy), 4, (0, 0, 255), -1)
    cv2.putText(img, f"A:{area:.0f} P:{perimeter:.0f}", (cx-40, cy-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
```

Hasil: setiap objek akan diberi informasi **luas (A)** dan **keliling (P)**.

---

## 4. Mengukur Panjang & Lebar (Bounding Box)

Dua jenis bounding box utama:

### a. **Bounding Rectangle**

```python
x, y, w, h = cv2.boundingRect(cnt)
cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
cv2.putText(img, f"W:{w} H:{h}", (x, y-5),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
```

### b. **Rotated Bounding Rectangle**

Jika objek miring, gunakan:

```python
rect = cv2.minAreaRect(cnt)
box = cv2.boxPoints(rect)
box = np.int0(box)
cv2.drawContours(img, [box], 0, (255, 0, 255), 2)
```

`rect` memberikan:

* `(cx, cy)` → pusat kotak
* `(w, h)` → panjang dan lebar
* `angle` → orientasi rotasi

---

## 5. Mengukur Radius dan Diameter (Lingkaran)

Untuk objek berbentuk bulat:

```python
(x, y), radius = cv2.minEnclosingCircle(cnt)
center = (int(x), int(y))
radius = int(radius)
cv2.circle(img, center, radius, (0, 255, 255), 2)
cv2.putText(img, f"r:{radius}", (center[0]-20, center[1]-10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 1)
```

---

## 6. Mengukur Orientasi Objek

Menggunakan **fitEllipse**:

```python
if len(cnt) >= 5:  # minimal 5 titik untuk elips
    ellipse = cv2.fitEllipse(cnt)
    cv2.ellipse(img, ellipse, (255, 0, 0), 2)
```

Nilai sudut elips dapat digunakan untuk menghitung **kemiringan objek**.

---

## 7. Menghitung Rasio dan Bentuk (Shape Descriptor)

### a. **Aspect Ratio**

Perbandingan panjang-lebar:

```python
x, y, w, h = cv2.boundingRect(cnt)
aspect_ratio = float(w)/h
```

* ~1 → persegi
* > 1 → horizontal
* <1 → vertikal

### b. **Extent**

Perbandingan antara luas objek dan luas bounding box:

```python
extent = float(area)/(w*h)
```

Semakin kecil nilai extent, semakin banyak ruang kosong di dalam bounding box.

### c. **Solidity**

Rasio antara luas kontur dengan luas convex hull:

```python
hull = cv2.convexHull(cnt)
hull_area = cv2.contourArea(hull)
solidity = float(area)/hull_area
```

* ~1 → bentuk padat
* <1 → bentuk berlekuk (misalnya tangan dengan jari)

### d. **Equivalent Diameter**

Diameter lingkaran dengan luas yang sama seperti kontur:

```python
equi_diameter = np.sqrt(4*area/np.pi)
```

---

## 8. Shape Matching (Perbandingan Bentuk)

Gunakan `cv2.matchShapes()` untuk membandingkan dua kontur:

```python
score = cv2.matchShapes(cnt1, cnt2, cv2.CONTOURS_MATCH_I1, 0.0)
print("Similarity:", score)
```

Semakin kecil skor → bentuk semakin mirip.

---

## 9. Kalibrasi Ukuran Nyata (Pixel ke Satuan Fisik)

Jika citra diambil dari kamera atau scanner, ukuran objek dapat dikonversi ke satuan cm/mm menggunakan **faktor skala**.

Contoh:

* Diketahui 100 piksel = 10 mm
  maka skala = 0.1 mm/piksel

```python
pixel_to_mm = 0.1
width_mm = w * pixel_to_mm
height_mm = h * pixel_to_mm
```

---

## 10. Aplikasi Praktis

Beberapa contoh penerapan shape & contour analysis:

| Bidang                   | Aplikasi                                             |
| ------------------------ | ---------------------------------------------------- |
| Industri                 | Pengukuran dimensi produk otomatis (Quality Control) |
| Kesehatan                | Pengukuran ukuran sel / tumor dalam citra mikroskop  |
| Pertanian                | Pengukuran luas daun, bentuk biji                    |
| Robotika                 | Object recognition dan tracking                      |
| Pengolahan citra digital | Segmentasi bentuk, shape classification              |

---

## 11. Contoh Lengkap Pengukuran Objek

```python
import cv2
import numpy as np

img = cv2.imread('shapes.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for i, cnt in enumerate(contours):
    area = cv2.contourArea(cnt)
    if area < 100:
        continue
    x, y, w, h = cv2.boundingRect(cnt)
    aspect_ratio = w / h
    perimeter = cv2.arcLength(cnt, True)
    M = cv2.moments(cnt)
    cx, cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    
    cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
    cv2.putText(img, f"Objek {i+1}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)
    cv2.putText(img, f"A={int(area)} AR={aspect_ratio:.2f}", (x, y+h+15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
    cv2.circle(img, (cx, cy), 4, (0,255,255), -1)

cv2.imshow('Measurement', img)
cv2.waitKey(0)
```

---

## 12. Kesimpulan

* **Contour analysis** dapat dimanfaatkan untuk **pengukuran dan klasifikasi bentuk**.
* Fitur penting yang bisa diambil antara lain:

  * Luas, keliling, rasio aspek, dan orientasi
  * Bentuk bounding box, elips, dan convex hull
  * Perbandingan antar objek menggunakan shape matching
* Kombinasi contour dengan kalibrasi skala memungkinkan pengukuran **dimensi nyata** objek.
