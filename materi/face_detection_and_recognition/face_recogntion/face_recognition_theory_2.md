# 🧠 **1. Apa itu LBPH Face Recognition?**

LBPH = **Local Binary Patterns Histogram**
Metode ini digunakan untuk *recognition* (mengenali “siapa”), bukan detection.

Konsep utama:

```
LBP → ekstraksi pola tekstur lokal
Histogram → representasi global wajah
Distance matching → siapa yang paling mirip
```

---

# 🎯 **2. Local Binary Pattern (LBP) — Cara Kerja Detail**

Setiap pixel wajah diproses seperti ini:

### 📌 Step 1: Ambil 8 tetangga pixel (3×3)

```
p0 p1 p2
p7  C p3
p6 p5 p4
```

`C` = center pixel
`p0–p7` = neighbor pixel

### 📌 Step 2: Bandingkan tiap tetangga dengan pusat:

```
if neighbor >= C:
    output = 1
else:
    output = 0
```

### 📌 Step 3: Urutan 8 bit membentuk 1 angka LBP

Contoh:

```
Tetangga:  10110011
Desimal:   179
```

Jadi 1 pixel → angka 0–255

### 🔍 Intinya:

LBP mendeskripsikan pola tekstur lokal di sekitar pixel.

Ini sangat cocok untuk wajah:

* mata = area gelap
* hidung = garis kontras
* pipi = area terang
* bibir = pola gelap terang tertentu

—

# 🧱 **3. Grid Histogram (H dalam LBPH)**

Setelah seluruh pixel dikonversi ke LBP values (0–255), gambar dibagi menjadi **grid**:

Misalnya 8×8 (64 region kecil).

Setiap region dihitung **histogram 256 bin**:

```
Hist(region_1) = [freq nilai 0, freq nilai 1, ..., freq nilai 255]
Hist(region_2) = ...
```

Kemudian semua histogram disatukan:

```
Feature Vector = H1 + H2 + ... + H64
```

Total panjang vector = 64 × 256 = **16,384 features**

➡ Ini representasi unik dari wajah yang mempertahankan pola lokal.

---

# 🏋‍♂️ **4. Training (Modeling)**

Training LBPH sebenarnya **sangat sederhana**.

Tidak ada learning. Tidak ada weights.
Yang disimpan hanya:

* histogram setiap orang
* label orang

Contoh:

```
Person1  → vector histogram (16k dim)
Person2  → vector histogram
dst...
```

Kalau ada 30 foto Person1: histogramnya dibuat rata-rata atau disimpan satu per satu.

---

# 🎯 **5. Predict (Cara LBPH mengenali orang)**

Saat wajah baru masuk:

1. Preprocess → LBP → histogram → feature vector
2. Bandingkan dengan semua model histogram orang lain
3. Pilih yang memiliki jarak (distance) paling kecil

### 📌 Jarak yang digunakan = Chi-Square distance

Secara matematis:

[
\chi^2 = \sum \frac{(X_i - Y_i)^2}{X_i + Y_i}
]

Semakin kecil nilai → semakin mirip.

OpenCV memberi:

```
label, confidence
```

Dimana:

* `label` = ID orang
* `confidence` = nilai jarak (semakin kecil semakin bagus)

---

# 📉 **6. Kenapa LBPH cocok untuk dataset kecil?**

Karena:

* Tidak perlu ratusan gambar
* Tidak perlu GPU
* Tidak sensitif pose
* Tidak sensitif pencahayaan *
* Bisa realtime

LBPH menangani variasi pencahayaan karena:

* perbandingan binary antara pixel & tetangganya (bukan nilai absolut)

---

# 🧪 **7. Kelebihan & Kekurangan LBPH**

## ✅ Kelebihan:

* Cepat (realtime CPU)
* Cocok untuk dataset kecil (30–100 gambar per orang)
* Tahan terhadap noise & shadow
* Mudah di-train ulang (tanpa retraining seluruh model)
* Mudah diimplementasikan

## ❌ Kekurangan:

* Tidak sebagus CNN modern
* Tidak bagus untuk pose miring (profil)
* Tidak bagus untuk ekspresi ekstrem
* Tidak bagus untuk jarak kamera jauh

---

# 📦 **Ringkasan Alur LBPH**

```
[Input wajah]
→ Convert grayscale
→ LBP transform (per pixel)
→ Bagi jadi grid
→ Histogram tiap grid
→ Concatenate histogram
→ Compare with known histograms
→ Distance paling kecil = orangnya
```

