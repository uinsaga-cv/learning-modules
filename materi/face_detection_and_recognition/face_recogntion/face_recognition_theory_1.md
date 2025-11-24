# 🧠 **1. Dasar Haar Cascade: Apa yang terjadi?**

Haar Cascade adalah algoritma **Face Detection**, bukan recognition.
Tugasnya = menemukan lokasi wajah.

Inti mekanismenya:

```
Input gambar (grayscale)
↓
Ekstrak ribuan fitur HAAR
↓
Seleksi fitur oleh AdaBoost
↓
Bangun banyak classifier kecil
↓
Disusun bertingkat (cascade)
↓
Scan gambar seperti sliding window
↓
Jika semua stage lulus → itu wajah
```

---

# 🧩 **2. Haar-like Features (Fitur Dasar)**

Haar-like feature adalah **pola kontras sederhana** seperti:

### 1. Two-rectangle (edge)

```
WHITE | BLACK
```

### 2. Three-rectangle (line)

```
BLACK | WHITE | BLACK
```

### 3. Four-rectangle (center-surround)

```
WHITE BLACK
BLACK WHITE
```

Fitur ini mendeteksi:

* perbedaan kontras mata vs pipi
* bayangan hidung
* pola terang-gelap wajah

➡ **Setiap fitur = hitung selisih brightness antara kotak-kotak.**

---

# ⚡ **3. Integral Image (Akselerasi Perhitungan)**

Jika fitur dihitung langsung = LAMBAT (ribuan fitur × ribuan posisi).

Solusinya: **Integral Image**

Jika `I(x, y)` = jumlah seluruh pixel dari (0,0) ke (x,y):

```
Sum area = I(br) - I(bl) - I(tr) + I(tl)
```

Dengan teknik ini:

* Hitung 100 ribu fitur hanya dalam **beberapa mikrodetik**.
* Inilah kenapa Haar Cascade sangat cepat walau di laptop lama.

---

# 🎯 **4. Training dengan AdaBoost**

Haar Cascade tidak memilih fitur secara manual.

Training dilakukan sbb:

### 1. Masukkan ribuan gambar:

* **Positive**: berisi wajah
* **Negative**: tidak berisi wajah

### 2. AdaBoost memilih fitur paling kuat

Dari **±180.000 fitur**, AdaBoost memilih mungkin hanya **200–600 fitur terbaik** yang benar-benar membedakan wajah dan bukan wajah.

### 3. Setiap fitur dipasangkan dengan threshold → menghasilkan Weak Classifier

```
if haar_feature_value > T:
    return face
else:
    return not_face
```

Ini masih lemah → tapi banyak classifier digabung menjadi kuat.

---

# 🧱 **5. Cascade Classifier (Tahapan Bertingkat)**

Fitur-fitur tidak dipakai sekaligus, tetapi disusun bertingkat (stage):

```
Stage 1 → Stage 2 → Stage 3 → ... → Stage N
```

Setiap stage adalah classifier yang makin ketat.

### ⚡ Cara kerja:

Saat sliding window berjalan:

1. **Stage 1** (cepaaaaat)

   * hanya ingin membuang background sebanyak mungkin
   * jika gagal → STOP → bukan wajah

2. **Stage 2**

   * lebih detail
   * jika gagal → STOP

3. **Stage 3**

   * makin detail

...

N. **Stage Terakhir**

* jika lolos semuanya → wajah

➡ 99% area gambar langsung dibuang di stage awal → sangat efisien.

---

# 🖼 **6. Sliding Window & Multi-Scale Detection**

Haar Cascade mendeteksi wajah di berbagai ukuran dengan:

1. Resize window → scan seluruh gambar
   atau
2. Resize gambar → window tetap

Window biasanya **24×24 pixel**, karena dataset training berukuran itu.

---

# 📉 **7. Kelebihan Haar Cascade**

* **Super cepat** (real-time di CPU biasa)
* Bisa berjalan di perangkat lama
* Tidak butuh GPU
* Tidak butuh banyak memori
* Akurat untuk kondisi normal (frontal face, cahaya oke)

---

# 📈 **8. Kekurangan Haar Cascade**

* Tidak akurat untuk pose miring
* Sensitif terhadap pencahayaan
* Tidak mendukung wajah profile
* Banyak false positive
* Tidak sekuat deep learning (SSD, MTCNN, YOLO-Face)

---

# 📦 **Ringkasan Alur Internal**

```
[Training]
  - Extract fitur Haar (ribuan)
  - AdaBoost pilih fitur terbaik
  - Susun cascade bertingkat

[Detection]
  - Convert to grayscale
  - Compute integral image
  - Sliding window scan
  - Tiap window diuji bertahap
  - Lulus semua stage → wajah
```
