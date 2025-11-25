# 🎯 **1. MODULE: Dataset Creation (Capture Wajah & Simpan ke Folder)**

## 📌 Tujuan

* Mengambil foto wajah dari webcam (atau gambar yang sudah ada).
* Mendektesi wajah menggunakan Haar Cascade.
* Men-crop dan menormalkan gambar.
* Menyimpannya dalam struktur dataset seperti:

```
dataset/
   person1/
       1.jpg
       2.jpg
       ...
   person2/
       1.jpg
       ...
```

## 🧠 **Bagaimana Cara Kerjanya (Internal Flow)**

1. **Load Cascade Classifier**

   ```python
   face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
   ```

   Ini model *pre-trained* yang mengenali pola edge & texture wajah.

2. **Capture Frame Webcam**

   ```python
   ret, frame = cap.read()
   ```

   Mengambil satu frame dari video stream (30–60 FPS).

3. **Convert ke Grayscale**
   Haar Cascade *wajib* bekerja di grayscale.

4. **Face Detection**

   ```python
   faces = face_cascade.detectMultiScale(gray, 1.3, 5)
   ```

   Outputnya adalah list koordinat bounding box:

   ```
   (x, y, w, h)
   ```

5. **Crop wajah**

   ```python
   face_img = gray[y:y+h, x:x+w]
   ```

6. **Resize**
   LBPH membutuhkan ukuran yang konsisten, biasa 100×100.

7. **Simpan file**

   ```python
   cv2.imwrite(f"dataset/person1/{count}.jpg", face_img)
   ```

---

# 🎯 **2. MODULE: Load Dataset untuk Training**

## 📌 Tujuan

* Membaca folder dataset
* Mengubah semua gambar ke grayscale array
* Memberikan label numerik

Contoh struktur data yang dihasilkan:

```python
images = [img1, img2, img3,...]
labels = [0, 0, 0, 1, 1, 1]
```

### 🧠 Internal Flow

1. **Scan folder dataset**
2. **Setiap folder = 1 orang**
3. **Mapping nama → label integer**

   ```
   person1 → 0
   person2 → 1
   ```
4. **Membaca gambar**

   ```python
   img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
   ```
5. **Append gambar & label**

LBPH sebenarnya bekerja pada **pattern histogram lokal**, jadi grayscale image tetap cocok.

---

# 🎯 **3. MODULE: Training Model LBPH**

## 📌 LBPH = Local Binary Pattern Histogram

Ini algoritma face recognition bawaan OpenCV.

### 🧠 Bagaimana LBPH bekerja?

1. **Local Binary Pattern (LBP)**
   Untuk setiap pixel:

   * Bandingkan pixel pusat dengan 8 tetangga
   * Jika tetangga >= pixel pusat → tulis 1
   * Jika < → tulis 0
   * Hasil = angka biner 8-bit → 0–255

   Contoh:

   ```
   1 0 1
   0 C 1
   1 0 1
   → 10110101 = 181
   ```

2. **Grid Histogram**

   * Gambar dibagi menjadi grid 8×8 atau 9×9
   * Setiap grid dihitung histogram nilai LBP (0–255)
   * Semua histogram disatukan → menjadi feature vector unik wajah

3. **Distance Matching**
   Model membandingkan histogram wajah baru dengan histogram data training menggunakan **Chi-Square Distance**.

---

# 🎯 **4. MODULE: Recognize Single Image**

### 🧠 Cara Kerja

1. Baca gambar
2. Deteksi wajah
3. Crop wajah
4. Resize
5. **Predict**

   ```python
   label, confidence = model.predict(face_img)
   ```

### 📌 Arti Confidence

* **Semakin kecil** → semakin akurat
* Biasanya threshold:

  ```
  0–60   → Sangat yakin
  60–80  → Mirip, tapi kurang yakin
  80+    → Tidak dikenali
  ```

---

# 🎯 **5. MODULE: Recognize Video (Real-time)**

### 🧠 Cara Kerjanya

Mirip dengan single image, tetapi dalam loop:

1. Ambil frame tiap 1/30 s
2. Deteksi wajah
3. Predict label + confidence
4. Tampilkan hasil pada frame (rectangle + nama)

### ⚠ Tantangan real-time:

* Pencahayaan berubah
* Pose berubah
* Wajah bergerak cepat
* Mungkin tidak selalu terdeteksi → harus handle “no face” gracefully

---

# 📦 Summary Alur Kerja Keseluruhan

```
[Capture Dataset]
        ↓
[Simpan dataset per person]
        ↓
[Load dataset]
        ↓
[LBPH Training]
        ↓
[Save model]
        ↓
[Recognize Image / Video]
```