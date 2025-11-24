# ✅ **5. PROSES TRAINING LBPH — PENJELASAN MENDALAM**

Tujuan modul ini:
Mengambil dataset (gambar-gambar wajah orang), kemudian melatih model **LBPH Face Recognizer** agar bisa mengenali wajah tersebut di masa mendatang.

---

# 🧠 **A. APA YANG TERJADI SELAMA TRAINING?**

Training LBPH melibatkan 3 proses inti:

1. **Ekstraksi fitur LBP** (Local Binary Pattern) dari setiap gambar wajah.
2. **Membuat histogram untuk setiap region wajah.**
3. **Menyimpan histogram tersebut sebagai representasi wajah** dalam file model (dataset_model.xml).

---

# 📍 **1. Local Binary Pattern (LBP) — Penjelasan Mendalam**

Konsep LBP sederhana tetapi sangat kuat.

### ✨ Prinsip LBP:

Untuk setiap piksel:

1. Ambil piksel pusat.
2. Bandingkan dengan 8 piksel tetangga (di sekelilingnya).
3. Jika piksel tetangga ≥ piksel pusat → beri nilai **1**
   Jika < piksel pusat → beri nilai **0**
4. Kombinasikan 8 bit tersebut → menjadi **angka 0–255**

Contoh sederhana:

```
Neighbours:   120  80  90
              200 [150] 140
              160 170  130
```

Bandingkan setiap tetangga dengan pusat (150):

```
120 < 150 → 0
80  < 150 → 0
90  < 150 → 0
200 > 150 → 1
140 < 150 → 0
160 > 150 → 1
170 > 150 → 1
130 < 150 → 0
```

Gabungkan jadi biner → `000100110`

Konversi ke desimal → **38**
Ini adalah **nilai LBP** untuk piksel tersebut.

---

### 📌 Kenapa LBP efektif untuk wajah?

Karena wajah punya pola tekstur yang kuat:

* perbedaan gelap-terang pada mata
* tepi hidung
* kontur bibir
* pola pipi dan rahang

LBP menangkap pola tekstur lokal, bukan warna, sehingga tahan terhadap:

✔ perubahan cahaya
✔ perbedaan warna kulit
✔ noise
✔ posisi kamera sedikit berubah

---

# 📍 **2. Membagi Gambar Menjadi Grid**

Wajah dibagi menjadi beberapa region, misalnya:

```
8 x 8 grid → total 64 region
```

Setiap region menghasilkan histogram 256 bin (karena nilai LBP = 0–255).

Maka:

```
1 wajah = 64 histogram = 64 × 256 angka
```

Inilah **ciri khas unik wajah**.

Kalau 10 foto wajah:

```
10 foto = 10 × (64 histogram)
```

---

# 📍 **3. Membuat Histogram di Setiap Region**

Pada setiap region:

* Hitung berapa banyak nilai LBP = 0
* Hitung berapa banyak nilai LBP = 1
* …
* Hitung berapa LBP = 255

Ini menghasilkan histogram seperti:

```
[20, 40, 15, 30, 0, 0, ..., 12]  (256 angka)
```

Histogram menunjukkan **karakteristik tekstur** region tersebut.

Contoh:

* Mata punya pola gelap-terang → histogram khas
* Hidung → tepi jelas → histogram berbeda
* The mouth → banyak shadow → histogram berubah

Karena itu, LBPH bisa membedakan wajah bahkan dengan cahaya berbeda.

---

# 📍 **4. Menggabungkan Semua Histogram**

Setelah semua region diproses:

```
histogram wajah = concat(hist1, hist2, ... hist64)
```

Jumlah total feature per wajah:

```
64 region × 256 bin = 16384 angka
```

(LBPH OpenCV bisa pakai konfigurasi lain, tetapi konsep sama.)

Inilah "penanda matematis" wajah.

---

# 📍 **5. Menyimpan Hasil Training**

Setelah semua gambar diproses:

```python
recognizer.write("dataset_model.xml")
```

XML ini berisi:

```
- semua histogram dari setiap orang
- label orang tersebut
- struktur grid
- konfigurasi radius, neighbors, grid X, grid Y
```

Contoh isi XML:

```
<opencv_storage>
    <LBPHFaceRecognizer>
        <radius>1</radius>
        <neighbors>8</neighbors>
        <grid_x>8</grid_x>
        <grid_y>8</grid_y>
        <histograms> ... </histograms>
    </LBPHFaceRecognizer>
</opencv_storage>
```

---

# 📍 **6. Model Tidak Menyimpan Gambar — hanya Fitur**

Penting!

LBPH **tidak menyimpan gambar asli**, hanya histogram.

Keuntungan:

✔ privasi lebih aman
✔ file model kecil
✔ prediksi lebih cepat
✔ robust terhadap variasi gambar

---

# 📍 **7. Bagaimana Training Menghadapi Banyak Foto?**

Jika untuk 1 label kamu punya 20 foto:

* LBPH mengekstrak histogram dari semua foto
* model menyimpan 20 histogram tersebut

Saat prediksi:

* LBPH membuat histogram frame baru
* lalu membandingkan dengan *semua histogram* di model

Jika histogram wajah baru paling mirip dengan foto milik "ID 3", maka hasilnya:

```
id = 3
confidence = nilai kedekatan histogram
```

---

# 📍 **8. Cara LBPH Mengukur Kecocokan**

LBPH memakai **distance metric**, biasanya:

### ✔ Chi-square distance:

[
\chi^2 = \sum \frac{(H1_i - H2_i)^2}{H1_i + H2_i}
]

Semakin kecil → semakin mirip.

### ✔ Confidence LBPH OpenCV

OpenCV mengubah distance menjadi "confidence":

* jarak kecil → confidence kecil → cocok
* jarak besar → confidence besar → tidak cocok

Aturan umum:

```
confidence < 60 → cocok (good match)
confidence 60–80 → ragu
confidence > 80 → unknown
```

---

# 📍 **9. Semakin Banyak Foto, Semakin Bagus**

Jika kamu punya:

* 1 foto → buruk
* 3 foto → lumayan
* 10 foto → bagus
* 30 foto → sangat bagus

LBPH butuh banyak variasi:

* kiri sedikit
* kanan sedikit
* cahaya berbeda
* ekspresi berbeda

---

# 📌 RINGKASAN TRAINING LBPH

| Tahap               | Penjelasan                      |
| ------------------- | ------------------------------- |
| grayscale           | menyederhanakan komputasi       |
| deteksi wajah       | crop ROI wajah                  |
| LBP                 | ambil pola tekstur lokal        |
| histogram           | representasi tekstur            |
| gabungkan histogram | signature unik wajah            |
| simpan model        | XML berisi histogram tiap wajah |

