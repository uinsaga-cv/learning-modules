# 🧩 **Praktikum: Analisis Kontur dan Pengukuran Objek dengan OpenCV**

---

## 🎯 **Tujuan Praktikum**

Setelah mengikuti praktikum ini, mahasiswa diharapkan mampu:

1. Memahami konsep dasar kontur (contour) pada citra digital.
2. Menggunakan fungsi `cv2.findContours()` dan `cv2.drawContours()` untuk mendeteksi bentuk objek.
3. Menghitung fitur geometris seperti luas, keliling, dan rasio aspek objek.
4. Menerapkan bounding box, convex hull, dan elips untuk analisis bentuk.
5. Melakukan pengukuran dimensi objek secara otomatis dari citra digital.

---

## 🧰 **Peralatan dan Bahan**

* Komputer dengan Python 3 dan OpenCV terinstal (`pip install opencv-python`)
* IDE: Visual Studio Code / Jupyter Notebook
* Gambar uji (misal: `shapes.png`, `coins.jpg`, `objects.png`)
* (Opsional) kamera atau citra hasil pemindaian objek nyata

---

## 🧠 **Dasar Teori Singkat**

* Kontur adalah garis yang menghubungkan titik-titik dengan intensitas sama.
* Untuk menemukan kontur, citra harus diubah ke **biner**.
* Informasi bentuk dapat diekstraksi dari kontur dengan menghitung:

  * Luas (`cv2.contourArea`)
  * Keliling (`cv2.arcLength`)
  * Pusat massa (`cv2.moments`)
  * Bounding box (`cv2.boundingRect`)
  * Convex hull (`cv2.convexHull`)
  * Aspect ratio, solidity, extent, dll.

---

## ⚙️ **Langkah Kerja**

### **Langkah 1 – Persiapan Citra**

1. Baca gambar menggunakan `cv2.imread()`
2. Ubah ke grayscale: `cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)`
3. Lakukan thresholding atau edge detection (Canny)

### **Langkah 2 – Deteksi Kontur**

1. Gunakan `cv2.findContours()` untuk mendapatkan kontur
2. Gambar semua kontur di atas citra asli dengan `cv2.drawContours()`

### **Langkah 3 – Analisis Bentuk**

1. Hitung luas, keliling, dan titik pusat setiap kontur
2. Gambarkan bounding box dan convex hull pada setiap objek
3. Tambahkan label objek dan nilai-nilai geometris di gambar

### **Langkah 4 – Analisis Lanjutan**

1. Hitung aspect ratio, extent, dan solidity
2. Gunakan `cv2.matchShapes()` untuk membandingkan dua bentuk
3. Tampilkan hasil visualisasi di jendela OpenCV

---

## 💻 **Contoh Kode Praktikum**

```python
import cv2
import numpy as np

# Baca dan ubah ke grayscale
img = cv2.imread('shapes.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Thresholding
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Temukan kontur
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Loop setiap kontur
for i, cnt in enumerate(contours):
    area = cv2.contourArea(cnt)
    perimeter = cv2.arcLength(cnt, True)
    x, y, w, h = cv2.boundingRect(cnt)
    M = cv2.moments(cnt)
    cx, cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    
    aspect_ratio = float(w)/h
    extent = float(area)/(w*h)
    hull = cv2.convexHull(cnt)
    hull_area = cv2.contourArea(hull)
    solidity = float(area)/hull_area
    
    cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
    cv2.circle(img, (cx,cy), 4, (0,0,255), -1)
    cv2.putText(img, f"Objek {i+1}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)
    cv2.putText(img, f"A={int(area)} AR={aspect_ratio:.2f}", (x, y+h+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)

cv2.imshow('Shape Analysis', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## 🧩 **Eksperimen Tambahan**

1. Ganti metode segmentasi:

   * `cv2.Canny()`
   * `cv2.adaptiveThreshold()`
2. Bandingkan hasil `RETR_EXTERNAL` dan `RETR_TREE`
3. Gunakan `cv2.approxPolyDP()` untuk mendeteksi jenis bentuk (segitiga, persegi, lingkaran)
4. Uji `cv2.matchShapes()` untuk mengukur kemiripan dua objek

---

## 🧾 **Tugas Mahasiswa**

### **Tugas Individu**

1. Gunakan gambar bebas (misalnya foto koin, daun, atau objek nyata).
2. Lakukan deteksi kontur dan tampilkan:

   * Bounding box
   * Convex hull
   * Titik pusat
3. Tampilkan hasil pengukuran:

   * Luas (px²)
   * Keliling
   * Rasio aspek
   * Solidity

### **Tugas Kelompok**

1. Buat program yang dapat:

   * Menghitung ukuran beberapa objek sekaligus
   * Mengklasifikasikan bentuk (segitiga, persegi, lingkaran)
   * Menampilkan total jumlah objek dan rata-rata luasnya
2. Simpan hasil analisis (data luas, keliling, bentuk) dalam file `.csv`
3. Buat laporan dalam format PDF yang berisi:

   * Penjelasan teori singkat
   * Flowchart program
   * Hasil tangkapan layar output
   * Analisis hasil

---