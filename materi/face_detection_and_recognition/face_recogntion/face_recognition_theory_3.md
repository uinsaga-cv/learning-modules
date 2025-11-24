# 🎯 **3. FACE ALIGNMENT (Dlib 68 Landmark)**

Face alignment berarti **meluruskan wajah** sebelum dikenali.

Tanpa alignment:

* wajah miring → LBPH/histogram jadi salah
* mata tidak sejajar
* hidung keluar dari area
* wajah tidak konsisten dengan dataset training

Dengan alignment:

* posisi mata, hidung, bibir → *fix*
* ukuran wajah seragam
* rotasi diperbaiki
* skala (jarak mata) distandardkan

Hasil akhirnya:

```
Raw face (miring, posisi acak)
↓
Aligned face (lurus, consistent)
```

---

# 🧠 **A. Cara Dlib Facial Landmark bekerja (Internal Algorithm)**

Dlib menggunakan model bernama **Shape Predictor** bernama:

```
shape_predictor_68_face_landmarks.dat
```

Model ini dilatih dengan metode **Ensemble of Regression Trees**.

Proses internalnya:

## 1. Haar/HOG Face Detection

Sebelum landmark ditemukan, wajah harus terdeteksi.
Dlib biasanya memakai **HOG + Linear SVM**.

## 2. Landmark Regression

Model shape predictor menargetkan **koordinat 68 titik**.

Contoh titik:

* 36–42 = mata kiri
* 42–48 = mata kanan
* 30 = hidung
* 48–67 = bibir

Model ini melakukan iterative regression:

```
Initial shape (mean face)
↓
Predict small offset
↓
Add offset to shape
↓
Predict lagi offset
↓
dst... ~10–20 kali
```

Setiap titik bergerak sedikit demi sedikit sampai mencapai lokasi landmark sebenarnya.

Ini sangat cepat dan akurat.

---

# ⭐ **B. 68 Landmark Index (Penting untuk Alignment)**

Berikut titik yang penting untuk alignment:

### Mata kiri:

```
36, 37, 38, 39, 40, 41
```

### Mata kanan:

```
42, 43, 44, 45, 46, 47
```

Untuk alignment, kita cukup pakai **titik tengah mata**.

---

# 🎯 **C. Cara Face Alignment dilakukan**

## Step 1: Temukan posisi kedua mata

```
LeftEyeCenter  = mean(landmarks[36..41])
RightEyeCenter = mean(landmarks[42..47])
```

## Step 2: Hitung sudut kemiringan wajah

```
dy = rightEyeY - leftEyeY
dx = rightEyeX - leftEyeX
angle = arctan(dy / dx)  (dalam derajat)
```

## Step 3: Rotate image untuk meluruskan mata

```
M = rotationMatrix(center, angle)
aligned = warpAffine(img, M)
```

Mata harus berada pada garis horizontal seperti ini:

```
Before:   /   (miring)
After:    —   (lurus)
```

## Step 4: Crop wajah pada posisi standar

Setelah rotasi → crop wajah berdasarkan bounding box wajah.

## Step 5: Resize ke ukuran konsisten, misalnya 100×100

Ini sangat penting untuk LBPH.

---

# 🔥 **D. Mengapa Face Alignment meningkatkan akurasi drastis?**

Karena LBPH dan metode histogram:

* sangat sensitif terhadap posisi pixel
* rotasi berubah → pola “tetangga” jadi berubah
* jarak mata berubah → region histogram berubah
* wajah miring → histogram tidak match dengan data training

Alignment “memperbaiki” hal ini.

Tanpa alignment, akurasi bisa **50–60%**
Dengan alignment, akurasi bisa **80–95%** untuk dataset kecil.

---

# 🧩 **E. Contoh Visual (Penjelasan Resmi)**

```
Wajah asli (raw)
— bisa miring, condong, jarak mata berbeda

↓ detect 68 landmark

Titik 36–47 → mata kiri & kanan
→ hitung sudut rotasi

↓ rotasi gambar

Wajah lurus (aligned)
— mata sejajar, proporsional

↓ crop + resize 100×100

Siap untuk LBPH / CNN
```

---

# ⚡ F. Kelebihan Face Alignment

* Peningkatan akurasi recognition
* Wajah konsisten meskipun miring
* LBPH lebih stabil
* Dataset lebih rapi
* Masking region (mata/hidung) dapat digunakan lebih baik

---

# 📉 G. Kekurangan

* Butuh file besar `shape_predictor_68_face_landmarks.dat`
  (96 MB)
* Lebih lambat dibanding hanya Haar
* Tidak bekerja pada wajah profile ekstrim
* Sensitif pada wajah yang tertutup (mask, kacamata hitam)

---

# 📦 H. Ringkasan Face Alignment

```
[Face Detection → Haar/HOG]
→ [Landmark Extraction → 68 Points]
→ [Calculate Eye Angle]
→ [Rotate Image]
→ [Crop Wajah]
→ [Resize]
→ Output: Aligned Face
```
