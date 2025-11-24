# Penjelasan lebih lanjut

 Dataset → Preprocessing → Face Detection → Feature / Representasi → Training (LBPH) → Penyimpanan & Load → Prediksi/Recognition → Evaluasi & Tuning → Deployment & Tips praktis.

## 1. Dataset (Pengumpulan dan Struktur)

Apa yang dilakukan

- Mengumpulkan gambar wajah per orang, menyimpan di folder `dataset/<person_name>/`.
- Tujuan: membuat label (class) bagi setiap orang; setiap folder merepresentasikan satu kelas.

Mengapa penting

- Model supervised (LBPH, Eigen, dsb.) butuh contoh diberi label.
- Variasi gambar (pose, lighting, ekspresi, background) membuat model lebih robust.

Detail teknis

- Struktur file: `dataset/andi/0.jpg, 1.jpg, ...`
- Label mapping: saat memuat folder, setiap folder diberi integer label (0..N-1). Mapping ini disimpan (mis. `labels.pkl`/`labels.json`).

Jebakan umum

- File kosong / corrupt → `cv2.imread` mengembalikan `None`. Selalu cek `os.path.exists()` dan size file.
- Nama folder berubah setelah training → label mapping mismatch saat inferensi. Simpan mapping persistently.

## 2. Preprocessing (Crop, Resize, Grayscale, Augmentation)

Langkah-langkah

1. Deteksi wajah → crop ROI (region of interest).
2. Resize ke ukuran seragam (mis. 200×200).
3. Konversi ke grayscale (LBPH & klasik bekerja di grayscale).
4. (Opsional) Normalisasi / Histogram equalization.
5. (Opsional) Augmentasi: rotasi kecil, flip, perubahan brightness.

Alasan

- Model memerlukan input ukuran tetap.
- Grayscale mengurangi dimensi dan sensitifitas warna; LBPH memakai pola lokal intensitas.
- Equalization membantu menanggulangi variasi pencahayaan.

Teknis: crop & resize

```python
face = gray[y:y+h, x:x+w]
face = cv2.resize(face, (200,200))
```

- Pastikan `y:y+h` dan `x:x+w` valid; cek bounds.

Augmentasi sederhana

- Flip horizontal `cv2.flip(face, 1)`
- Brightness adjust: `face * alpha + beta` (clip ke 0..255)
- Rotasi kecil via `cv2.getRotationMatrix2D`

Jebakan

- Meng-resize terlalu kecil (<=100px) → kehilangan detail tekstur untuk LBPH.
- Crop yang terlalu ketat memotong fitur penting (mata, hidung) atau memasukkan terlalu banyak background.

## 3. Face Detection (Haarcascade / DNN)

Fungsi

- Menemukan bounding box wajah `(x,y,w,h)` pada gambar.

Haarcascade (OpenCV) — ringkasan

- Menggunakan fitur Haar-like (edge/line) dan classifier cascade (AdaBoost).
- Cepat, ringan, cocok untuk real-time pada CPU.
- Parameter penting: `scaleFactor`, `minNeighbors`, `minSize`.

  - `scaleFactor=1.1` berarti tiap iterasi window diskalakan 10%.
  - `minNeighbors` mengontrol berapa banyak kotak deteksi yang harus "setuju" — nilai lebih tinggi mengurangi false positives.
  - `minSize` mencegah deteksi objek sangat kecil.

DNN detector (lebih akurat)

- Menggunakan model pre-trained (Caffe/TensorFlow) — lebih akurat terhadap pose & lighting, tapi lebih berat.
- Implementasi: `cv2.dnn.readNetFromCaffe()` + forward pass.

Kesalahan umum

- Tidak memuat cascade XML (path salah) → no detections.
- Parameter `minSize` terlalu besar → wajah kecil tidak terdeteksi.
- Banyak false positives → atur `minNeighbors` naik.

## 4. Representasi / Feature: LBPH (Local Binary Patterns Histogram)

Inti konsep LBPH

- Untuk setiap pixel, bandingkan intensitasnya dengan tetangganya (biasanya 8 tetangga) → hasil bit (0/1) membentuk kode (0–255).
- Kode ini menunjukkan pola lokal (edges/textures).
- Gambar dibagi ke grid (mis. 8×8 cells); untuk tiap cell dihitung histogram LBP.
- Gabungkan histogram tiap cell → descriptor akhir (vektor fitur).
- Untuk pengenalan, bandingkan histogram (mis. dengan jarak Euclidean/chi-square); nilai distance disebut _confidence_.

Kenapa efektif

- Sensitif pada tekstur lokal (mis. area mata, hidung, mulut) dan tahan terhadap variasi pencahayaan kecil.
- Ringan, cocok untuk data kecil.

Parameter LBPH

- `radius` (berapa jauh tetangga dilihat, default 1)
- `neighbors` (berapa titik sampel, default 8)
- `grid_x`, `grid_y` (jumlah cell horizontal & vertikal)
- Pemilihan pengaturan memengaruhi dimensi histogram dan kepekaan model

Implementasi OpenCV

```python
recognizer = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8)
recognizer.train(faces, np.array(labels))
```

Confidence interpretation

- OpenCV LBPH memberi nilai `confidence` (bukan probabilitas): semakin kecil → semakin mirip.
- Thresholding: tentukan ambang (mis. 50–80) berdasarkan validasi.

## 5. Training (Proses & Data Structures)

Apa yang terjadi

- Fungsi `train(faces, labels)` menerima list/array gambar grayscale dan array label integer.
- LBPH mengonversi setiap gambar menjadi fitur histogram dan menyimpan histograms per kelas (secara internal).
- Training LBPH adalah _instance-based_ (mencatat statistik/representasi tiap sample), bukan neural network dengan epoch.

Data preparation

- `faces` harus numpy array atau list of 2D arrays.
- `labels` harus 1D numpy array of ints.

Skenario kesalahan

- Mixed image sizes → `train` butuh ukuran seragam; resize sebelum train.
- `faces` mengandung `None` → error. Periksa file read success.

## 6. Penyimpanan & Loading Model

Mengapa

- Setelah training, model disimpan agar tidak perlu train ulang tiap kali.

Format

- `recognizer.save("face_model.yml")` atau `.xml`
- Label map disimpan terpisah (pickle/json) karena hanya recognizer menyimpan angka label, bukan nama.

Loading

```python
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("face_model.yml")
label_map = pickle.load(open("labels.pkl", "rb"))
```

Jebakan

- Versi OpenCV berbeda → format file mungkin tidak kompatibel. Simpan juga script dan versi OpenCV.

## 7. Prediksi / Recognition (Inference)

Alur

1. Ambil frame / gambar.
2. Deteksi wajah → crop → resize → grayscale.
3. `label, confidence = recognizer.predict(face_roi)`
4. Ambil `name = label_map[label]` jika `confidence` di bawah threshold.

Interpretasi confidence

- Tidak baku; perlu validasi empiris.
- Lakukan validasi ► buat set validasi/hold-out, catat distribusi confidence benar vs salah → pilih threshold.

Handling unknown faces

- Jika `confidence > threshold` → tandai sebagai _Unknown_.
- Untuk aplikasi nyata, tambah mekanisme _rejection_ dan fallback.

Latency

- Untuk video real-time, deteksi lebih berat dari predict; optimasi dengan:

  - Resize frame sebelum deteksi
  - Deteksi tiap N frame
  - Gunakan DNN yang dioptimalkan atau GPU bila perlu

## 8. Evaluasi & Metrics

Metode

- Split dataset: Train / Validation / Test (mis. 70/15/15)
- Metrics: accuracy, precision, recall, confusion matrix
- Untuk verification (1:1): ROC curve, EER (equal error rate)

Cross-validation

- K-fold CV (jika dataset kecil) untuk menghindari overfitting pada beberapa orang tertentu.

Analisis kesalahan

- Ambil false positives / false negatives → tinjau gambar: lighting, occlusion, pose.

## 9. Parameter Tuning & Praktik Baik

Face detection

- `scaleFactor` 1.05–1.3 (1.1 default)
- `minNeighbors` 3–6 (nilai lebih tinggi kurangi false positives)
- `minSize` set sesuai resolusi input

LBPH

- `grid_x, grid_y`: default 8×8; kurangi untuk gambar kecil
- `radius` & `neighbors`: default 1 & 8 oke untuk mulai

Threshold

- Tentukan lewat validasi, bukan tebakan.

Augmentasi

- Sangat membantu saat data terbatas: flip, brightness, small rotation.

## 10. Troubleshooting Umum (Praktis)

- `cv2.error !_src.empty()` → `cv2.imread` gagal → cek path / file corrupt.
- `AttributeError: module 'cv2' has no attribute 'face'` → install `opencv-contrib-python`.
- Hasil pengenalan buruk → periksa:

  - dataset tidak cukup variatif
  - wajah terlalu kecil (resize input)
  - model perlu retraining / augmentasi

- Model bisa bias ke kondisi tertentu (lighting/background) → tambahkan variasi.

## 11. Keamanan, Etika, Lisensi

- Pastikan penggunaan gambar memenuhi hak cipta dan privasi.
- Untuk riset akademik: gunakan dataset yang berlisensi untuk riset (LFW, CelebA, dsb.) atau dataset yang Anda miliki izin.
- Untuk aplikasi produksi di area sensitif (mis. biometrik), ikuti regulasi lokal (biometric laws).

## 12. Extensions / Next Steps (kalau mau lebih lanjut)

- Ganti representasi: gunakan embedding deep learning (FaceNet, ArcFace) untuk performa jauh lebih baik.

  - Pipeline: detect → align → embed → classifier (SVM / k-NN) atau thresholding.

- Face alignment: deteksi landmark (mata, hidung) → rotasi & transform agar wajah dinormalisasi (membantu akurasi).
- Gunakan face recognition library seperti `face_recognition` (dlib-based) untuk prototyping cepat.
- Jika banyak kelas (ratusan/lebih), deep embeddings + classifier lebih efisien.

## Contoh: Walkthrough kode (singkat) — apa yang terjadi di tiap baris

Ambil potongan sederhana:

```python
img = cv2.imread("test.jpg")             # baca file ke BGR numpy array
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # ubah ke grayscale
faces = cascade.detectMultiScale(gray, 1.3, 5) # deteksi wajah

for (x,y,w,h) in faces:
    face = gray[y:y+h, x:x+w]           # crop ROI
    face = cv2.resize(face, (200,200))  # resize -> ukuran konsisten
    label, confidence = recognizer.predict(face) # prediksi LBPH
```

- `detectMultiScale` menghasilkan koordinat.
- Crop & resize memastikan input ke recognizer sesuai ukuran saat training.
- `predict` membandingkan histogram wajah dengan representasi yang disimpan selama training.

---

Kalau mau, saya bisa:

- Buat dokumen PDF dengan penjelasan + gambar ilustrasi alur (detect → preprocess → train → predict).
- Buat notebook Jupyter yang menjalankan setiap langkah dan menampilkan visual: contoh crop, histogram LBP, distribusi confidence, contoh false positive.
- Atau langsung tulis modul Python yang menyertakan logging / pengecekan error otomatis (robust), termasuk fungsi `prepare_dataset()`, `train_model()`, `evaluate()` dan `infer_image()/infer_video()`.

Mau saya buat salah satu? Pilih: PDF / Notebook / Modul Python siap pakai.
