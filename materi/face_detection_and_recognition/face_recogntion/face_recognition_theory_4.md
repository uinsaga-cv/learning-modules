# ✅ **4. TEST RECOGNIZE VIDEO — PENJELASAN MENDALAM**

Tujuan modul ini:
Menggunakan kamera (atau file video) untuk **mendeteksi wajah** dan **mengenali identitas** berdasarkan model LBPH yang sudah kita latih.

---

# 🧠 **A. ALUR BESAR PROSES FACE RECOGNITION DI VIDEO**

Ketika video berjalan (frame per frame), proses berikut terjadi:

1. Kamera menangkap satu frame (gambar).
2. Frame dikonversi ke grayscale.
3. Haar Cascade mendeteksi posisi wajah dalam frame.
4. Setiap wajah dipotong (cropped).
5. LBPH predictor memproses wajah tersebut → mengubah menjadi histogram lokal.
6. Model membandingkan histogram frame saat ini dengan histogram wajah di dataset.
7. Menghasilkan:

   * **label** → ID orang
   * **confidence** → seberapa yakin model
8. Hasil ditampilkan: nama + kotak wajah.

---

# 🧩 **B. PENJELASAN RINCI TIAP BAGIAN DALAM KODE**

Berikut struktur umum kode pengenalan video:

```python
import cv2

# Load Haar Cascade
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Load LBPH trained data
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("dataset_model.xml")

cap = cv2.VideoCapture(0)   # pakai webcam
```

---

## 📍 **1. VideoCapture() — Menangkap Frame**

`cv2.VideoCapture(0)`

* `0` = kamera default
* jika file video → `cv2.VideoCapture("video.mp4")`

OpenCV menangkap frame demi frame.

Secara internal:

* Kamera mengirim raw frames.
* OpenCV buffer → menahan frame terbaru.
* Setiap `cap.read()` mengambil frame saat ini.

---

## 📍 **2. Konversi ke Grayscale**

```python
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
```

Kenapa harus grayscale?

* Haar Cascade dan LBPH bekerja **hanya pada luminance** (intensitas cahaya).
* Grayscale mempercepat komputasi ×4 lebih cepat.
* Menghilangkan noise warna yang tidak dibutuhkan.

Secara teknis:

* Mengambil channel BGR → dihitung ulang jadi 1 channel
* Formula = 0.299R + 0.587G + 0.114B

---

## 📍 **3. Deteksi Wajah — Haar Cascade**

```python
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
```

Penjelasan internalnya:

### **Haar Cascade bekerja dengan cara:**

1. Sliding window berjalan di seluruh gambar.
2. Pada tiap window, fitur HAAR dihitung:

   * edge feature
   * line feature
   * center-surround
3. Adaboost memilih fitur paling penting.
4. Cascade classifier:

   * Tahap awal: sederhana, untuk menolak background.
   * Tahap akhir: kompleks, untuk validasi wajah.

### Parameter penting:

* **scaleFactor=1.2**: ukuran window berubah 20% tiap iterasi (multiscale detection)
* **minNeighbors=5**: jumlah validasi fitur sebelum dianggap wajah
* output → banyaknya wajah & koordinat bounding box

---

## 📍 **4. Cropping Wajah**

```python
for (x, y, w, h) in faces:
    roi_gray = gray[y:y+h, x:x+w]
```

Kenapa cropping?

* LBPH harus diberi input wajah *saja*, bukan background.
* Cropping memotong area yang terdeteksi sebagai wajah.

---

# 🧠 **5. LBPH RECOGNIZER — PROSES INTERNAL**

```python
id, confidence = recognizer.predict(roi_gray)
```

Di sini bagian paling penting.

### LBPH (Local Binary Patterns Histogram) melakukan:

### ✔ 1. Membagi wajah menjadi grid misalnya 8×8

### ✔ 2. Pada tiap grid, membuat **LBP binary pattern**

Contoh:

* ambil piksel pusat
* bandingkan dengan piksel sekitar
* jika lebih besar: 1
* jika lebih kecil: 0
  → menghasilkan *binary number* 8 bit.

### ✔ 3. Mengubah binary jadi desimal → “signature” pola tekstur wajah

### ✔ 4. Menghitung histogram untuk setiap region

Misalnya histogram tiap grid memiliki 256 bin.

### ✔ 5. Menggabungkan semua histogram

→ menjadi **1 vektor fitur** representasi wajah.

---

# 📏 **6. Cara LBPH Menghitung Kecocokan**

Saat prediksi:

* LBPH membuat histogram dari wajah baru.
* Histogram ini dibandingkan dengan seluruh histogram di dataset.

Metode yang biasa dipakai:

* **Chi-square distance**
* **Euclidean distance**

Semakin kecil distance → semakin mirip.

Outputnya:

* **label (id)** → identitas wajah
* **confidence** → seberapa kecil jaraknya (semakin kecil semakin mirip)

Catatan:

* OpenCV LBPH:

  * nilai kecil = cocok
  * nilai besar = tidak cocok
  * threshold umum = 50–80

---

# 🟥 **7. Menentukan Nama Orang Berdasarkan ID**

```python
if confidence < 60:
    name = names[id]
else:
    name = "Unknown"
```

Internal:

* Jika wajah mirip dengan database → confidence rendah.
* Jika tidak cocok → model return confidence besar → unknown.

---

# 🟩 **8. Gambarkan Hasil ke Video**

```python
cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
cv2.putText(frame, name, (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
```

OpenCV menggambar:

* bounding box
* nama
* confidence (opsional)

OpenCV merender frame demi frame → terlihat seperti video.

---

# 🎥 **9. Loop Berjalan Terus Sampai Di-Stop**

```python
if cv2.waitKey(1) & 0xFF == ord('q'):
    break
```

* `waitKey(1)` membaca input keyboard setiap 1 ms.
* `q` untuk keluar dari loop.

---

# 🧽 **10. Release Resource**

```python
cap.release()
cv2.destroyAllWindows()
```

Membersihkan:

* koneksi kamera
* window OpenCV

---

# 📌 RINGKASAN INTERNAL PROCESS

| Tahap                    | Mekanisme Internal                   |
| ------------------------ | ------------------------------------ |
| **Frame Capture**        | Ambil frame dari buffer kamera       |
| **Grayscale**            | Konversi matriks BGR → 1 channel     |
| **Haar Cascade**         | Sliding window + AdaBoost classifier |
| **Crop ROI**             | Ambil area wajah saja                |
| **LBPH Extraction**      | Hitung LBP → histogram region        |
| **Compare with Dataset** | Chi-square/Euclidean distance        |
| **Output**               | label + confidence                   |
| **Render**               | draw rectangle + nama                |


