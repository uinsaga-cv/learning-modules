# FACE RECOGNITION & FACE DETECTION

# 🧩 **1. Pengertian Face Detection & Face Recognition**

### **Face Detection**

- Menemukan keberadaan wajah dalam gambar.
- Output: bounding box (x, y, w, h).

### **Face Recognition**

- Mengidentifikasi _siapa_ orang tersebut.
- Output: ID atau nama orang.

Perbedaan utama:

| Face Detection      | Face Recognition                      |
| ------------------- | ------------------------------------- |
| Menemukan wajah     | Mengenali identitas                   |
| Tidak butuh dataset | Butuh dataset training                |
| Object detection    | Pattern matching / feature extraction |
| Cepat               | Lebih kompleks                        |

---

# 🧩 **2. Alur Lengkap Face Recognition Modern**

```
[1] Face Detection
        ↓
[2] Face Alignment
        ↓
[3] Feature Extraction (LBP / PCA / LDA / CNN)
        ↓
[4] Classification / Recognition
```

---

# 🧩 **3. Face Detection (Haar Cascade)**

### Cara kerja Haar:

- Menggunakan fitur Haar (kotak terang-gelap).
- Ditraining dengan ratusan ribu weak classifier (AdaBoost).
- Sliding window memindai seluruh gambar.

### Kelebihan:

- Sangat cepat.
- Ringan (bisa jalan di laptop lama).

### Kekurangan:

- Tidak akurat untuk rotasi.
- Sensitif terhadap posisi wajah.

---

# 🧩 **4. Face Alignment (Dlib 68 Landmark)**

Face alignment membuat wajah “lurus” sebelum dikenali.

Langkah:

```
1. Deteksi wajah (HOG/SVM)
2. Ambil 68 facial landmarks
3. Hitung titik tengah mata
4. Hitung sudut kemiringan wajah
5. Rotasi wajah agar mata sejajar horizontal
6. Crop & resize
```

Mengapa alignment sangat penting?

- LBPH, EigenFace, FisherFace sensitif terhadap rotasi.
- Tanpa alignment → akurasi rendah.
- Dengan alignment → akurasi naik drastis (60% → 90%).

---

# 🧩 **5. Ekstraksi Fitur: LBPH**

Konsep utama:

### Local Binary Pattern

Untuk setiap piksel:

```
Bandingkan piksel tetangga dengan pusat:
>= pusat → 1
< pusat → 0
```

Membentuk nilai biner 8-bit → 0–255.

### LBPH Steps:

1. Gambar wajah dibagi menjadi grid (mis. 8×8).
2. Setiap region membuat histogram nilai LBP.
3. Semua histogram digabung → "signature wajah".
4. Signature disimpan sebagai fitur.

Keunggulan LBPH:

- Tahan terhadap perubahan cahaya.
- Tahan noise.
- Tidak perlu dataset besar.
- Cepat.

---

# 🧩 **6. Ekstraksi Fitur: EigenFace (PCA)**

EigenFace adalah metode **dimensionality reduction**.

Langkah:

1. Semua wajah diratakan (flatten) menjadi vektor.
2. Hitung covariance matrix.
3. Ambil eigenvector terbesar (principal components).
4. Proyeksikan wajah ke ruang eigenface.

Konsep mirip:

```
Wajah direduksi menjadi kombinasi linear wajah-wajah dasar (eigenfaces).
```

Kelebihan:

- Cepat
- Matematika kuat

Kekurangan:

- Sangat sensitif terhadap cahaya
- Sensitif terhadap rotasi

---

# 🧩 **7. Ekstraksi Fitur: FisherFace (LDA)**

FisherFace menggunakan **Linear Discriminant Analysis**:

Tujuan:

- Memaksimalkan jarak antar kelas wajah
- Meminimalkan jarak intra-kelas

Lebih robust dibanding EigenFace.

Namun:

- Butuh lebih banyak data
- Butuh semua kelas punya jumlah data yang sama

---

# 🧩 **8. Perbandingan LBPH vs EigenFace vs FisherFace**

| Metode         | Ketahanan Cahaya | Ketahanan Rotasi | Dataset Diperlukan     | Kecepatan    | Akurasi |
| -------------- | ---------------- | ---------------- | ---------------------- | ------------ | ------- |
| **LBPH**       | ✔✔✔ tinggi       | sedang           | kecil                  | sangat cepat | baik    |
| **EigenFace**  | ✘ buruk          | buruk            | sedang                 | cepat        | sedang  |
| **FisherFace** | ✔ sedang         | sedang           | besar (butuh seimbang) | sedang       | bagus   |

Kesimpulan:

- **LBPH = terbaik untuk pemula & aplikasi real-time**
- **FisherFace = stabil untuk dataset besar**
- **EigenFace = untuk demonstrasi PCA, kurang praktis**

---

# 🧩 **9. Training Model Face Recognition**

```
1. Kumpulkan dataset wajah
2. Face detection → crop wajah
3. Face alignment
4. Resize
5. Simpan dataset
6. Latih LBPH/Eigen/Fisher
7. Simpan model .xml
```

---

# 🧩 **10. Testing Model**

**Input:**

- gambar atau frame video

**Langkah:**

1. Deteksi wajah
2. Align wajah
3. Ekstrak fitur
4. Bandingkan dengan fitur training
5. Kembalikan:

   - ID hasil match
   - nilai confidence

Confidence LBPH:

- < 60 → sangat cocok
- 60–80 → ragu
- > 80 → unknown

---

# 🧩 **11. Tantangan Face Recognition Tradisional**

- sensitif terhadap:

  - pose
  - pencahayaan
  - wajah tertutup
  - noise kamera

- butuh banyak foto untuk hasil akurat
- tidak bisa face spoofing (foto/gambar)

Solusi modern:

- FaceNet
- ArcFace
- DeepFace
- InsightFace

Jika ingin, saya bisa buat modul deep learning juga.

---

# 🧩 **12. Studi Kasus: Sistem Absensi Berbasis Wajah**

Komponen:

1. Kamera → webcam
2. Face detection → Haar
3. Face alignment → Dlib
4. Feature extraction → LBPH
5. Database mahasiswa
6. Penyimpanan kehadiran

Flow:

```
Input kamera
→ deteksi wajah
→ align
→ recognize (ID)
→ cek database
→ simpan absensi
```

---

# 🧩 **13. Struktur Folder Dataset Face Recognition**

```
dataset/
    person_1/
        1.jpg
        2.jpg
        3.jpg
    person_2/
        1.jpg
        2.jpg
        3.jpg
model/
    lbph_model.xml
    labels.pickle
```

---

# 🧩 **14. Tips Membuat Dataset**

Minimal 20–50 foto per orang:

✔ depan
✔ miring kiri
✔ miring kanan
✔ ekspresi berbeda
✔ cahaya berbeda
✔ jarak kamera berbeda

Untuk akurasi tinggi.

---

# 🧩 **15. Penutup: Konsep Kunci yang Wajib Dipahami Mahasiswa**

1. **Detection ≠ Recognition**
2. Alignment adalah kunci akurasi
3. LBPH : tekstur wajah (cahaya robust)
4. EigenFace : PCA, dimensi turun
5. FisherFace : memisahkan kelas wajah
6. Training = ekstraksi fitur + simpan ke model
7. Testing = membandingkan histogram/fitur
