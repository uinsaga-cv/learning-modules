# Haar Method

## 🧠 Inti Gagasan

Algoritma **Haar Cascade** mendeteksi wajah dengan **mempelajari pola visual khas wajah manusia** — seperti:

* Mata biasanya lebih gelap daripada pipi,
* Hidung lebih terang dari sekitarnya,
  dan seterusnya.

Jadi, komputer tidak mengenali “wajah” secara semantik, tapi **mengenali pola kontras terang-gelap tertentu.**

---

## ⚙️ Cara Kerjanya (Langkah demi langkah)

### 1. **Fitur Haar (Haar-like features)**

Fitur ini adalah **pola persegi sederhana** yang membandingkan kecerahan antara dua area.

Contohnya:

| Jenis fitur | Maknanya                                                             |
| ----------- | -------------------------------------------------------------------- |
| ▒█          | Area gelap di atas terang — cocok untuk mendeteksi mata di atas pipi |
| █▒          | Terang di atas gelap — cocok untuk hidung                            |
| █▒█         | Terang–gelap–terang — cocok untuk mendeteksi tepi hidung             |

➡️ Algoritma akan menghitung **selisih rata-rata intensitas** antara area putih dan hitam.

---

### 2. **Integral Image**

Agar cepat menghitung perbedaan terang-gelap untuk ribuan posisi, algoritma menggunakan **Integral Image** — semacam peta kumulatif dari jumlah pixel.
Dengan ini, perhitungan perbandingan terang-gelap bisa dilakukan **hanya dalam 4 operasi matematis** (cepat banget 🔥).

---

### 3. **Training (dengan banyak contoh)**

Algoritma dilatih menggunakan:

* Ribuan **gambar wajah** (positif)
* Ribuan **gambar bukan wajah** (negatif)

Dari situ dipilih fitur-fitur yang paling berguna untuk membedakan wajah vs bukan wajah.

Namun — jumlah fitur bisa mencapai **ratusan ribu**! Maka dibutuhkan langkah berikut:

---

### 4. **Adaboost**

Adaboost adalah teknik untuk:

* **Memilih fitur-fitur paling kuat (efektif)**,
* **Menggabungkan banyak fitur lemah menjadi satu detektor kuat.**

Dengan Adaboost, hanya sebagian kecil fitur yang dipakai untuk mendeteksi wajah dengan akurat.

---

### 5. **Cascade Classifier**

Setelah fitur-fitur terbaik ditemukan, mereka disusun dalam bentuk **tahapan (cascade)**:

Contohnya:

1. Tahap 1: cek pola gelap-terang dasar (cepat, singkirkan area bukan wajah)
2. Tahap 2: cek fitur lebih rinci
3. Tahap 3: fitur lebih kompleks
4. dan seterusnya...

➡️ Dengan sistem ini, **area gambar yang jelas bukan wajah langsung dibuang di tahap awal**.
Hanya area yang "mirip wajah" lanjut ke tahap berikutnya → hasilnya cepat dan efisien.

---

## 📸 6. Deteksi Wajah di OpenCV

OpenCV menyediakan classifier hasil training (file `.xml`), misalnya:

```python
import cv2
import os

xmlPath = os.path.join(".", "assets/xml", "haarcascade_frontalface_default.xml")
face_cascade = cv2.CascadeClassifier(xmlPath)

imgPath = os.path.join(".", "img", "children.jpg")
image = cv2.imread(imgPath)

imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(imageGray, scaleFactor=1.1, minNeighbors=5)

for x, y, w, h in faces:
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 5)

cv2.imshow("children", image)
cv2.waitKey(0)

```

xml files: [Haar Algorithm](https://github.com/opencv/opencv/tree/master/data/haarcascades)

---

## 💡 Kelebihan & Kekurangan

| Kelebihan                            | Kekurangan                                                                         |
| ------------------------------------ | ---------------------------------------------------------------------------------- |
| Cepat dan ringan (efisien real-time) | Kurang akurat pada pencahayaan, rotasi, atau ekspresi wajah yang berbeda           |
| Tidak butuh GPU                      | Sulit mendeteksi wajah dari samping                                                |
| Mudah digunakan di OpenCV            | Digantikan oleh metode modern seperti **HOG** dan **Deep Learning (CNN/SSD/YOLO)** |

---

## 🔍 Intinya:

**Haar Cascade** = cara klasik tapi cerdas mendeteksi wajah dengan **mengenali pola terang-gelap** dan menyaring area gambar lewat **tahapan cepat (cascade)**.
Masih sering dipakai untuk sistem sederhana, webcam, atau aplikasi ringan.

---

# Haar Training Algorithm

## 🧠 Tujuan Proses Training

Tujuan utamanya:

> Mengajarkan komputer **membedakan area wajah dan bukan wajah** berdasarkan pola terang–gelap (fitur Haar).

---

## ⚙️ 1. Persiapan Data

Training butuh dua kelompok data:

| Jenis Data                     | Isi                                    | Contoh                                                  |
| ------------------------------ | -------------------------------------- | ------------------------------------------------------- |
| **Positif (positive samples)** | Gambar yang **mengandung wajah**       | foto wajah dari berbagai orang, posisi, dan pencahayaan |
| **Negatif (negative samples)** | Gambar yang **tidak mengandung wajah** | pemandangan, gedung, hewan, tekstur, dll                |

Biasanya setiap gambar wajah di-*crop* jadi ukuran kecil, misalnya **24×24 piksel** (ukuran fitur dasar Haar).

---

## 🧩 2. Ekstraksi Fitur Haar

Dari setiap patch 24×24 piksel, algoritma menghasilkan **ratusan ribu fitur Haar**, misalnya:

* Dua-rectangle (gelap–terang),
* Tiga-rectangle (terang–gelap–terang),
* Empat-rectangle (checkerboard).

Untuk mempercepat perhitungan intensitas terang–gelap, digunakan **Integral Image**.
Dengan integral image, selisih kecerahan antara dua area bisa dihitung hanya dalam **4 operasi** (sangat cepat).

---

## 💪 3. Adaboost (Adaptive Boosting)

Jumlah fitur yang dihasilkan sangat besar (bisa >100.000).
Kita tidak mungkin pakai semuanya, jadi dilakukan **seleksi fitur** menggunakan **Adaboost**.

🧩 Cara kerjanya:

1. Setiap fitur dianggap sebagai *weak classifier* (klasifier lemah).
   → Misal: “jika area atas lebih gelap dari bawah, mungkin wajah.”
2. Adaboost **menilai seberapa baik setiap fitur memisahkan data wajah dan bukan wajah.**
3. Fitur-fitur dengan performa tinggi diberi bobot lebih besar.
4. Kemudian Adaboost **menggabungkan banyak fitur lemah menjadi satu classifier kuat** (strong classifier).

➡️ Hasilnya: hanya fitur-fitur paling informatif yang dipilih (misalnya beberapa ratus dari ratusan ribu).

---

## 🏗️ 4. Cascade Classifier

Setelah didapatkan ratusan strong classifier, OpenCV menyusunnya jadi **beberapa tahap (stages)** dalam bentuk **cascade**.

Ibarat gerbang berlapis:

* **Stage 1**: sangat sederhana → cepat menolak area bukan wajah.
* **Stage 2–N**: makin ketat dan detail → hanya area yang mirip wajah lolos.

Jika area gambar gagal di satu tahap saja → **langsung dibuang**, jadi proses sangat efisien.

Contoh:

| Stage | Jumlah fitur | Tujuan                                        |
| ----- | ------------ | --------------------------------------------- |
| 1     | 2–5 fitur    | Filter kasar (apakah ada sesuatu mirip wajah) |
| 2     | 20 fitur     | Periksa pola mata–hidung                      |
| 3     | 50 fitur     | Cek struktur wajah lebih kompleks             |
| …     | …            | Semakin detail di tiap tahap                  |

Biasanya totalnya bisa sampai **20–25 stage**.

---

## 🧾 5. Hasil Akhir → File XML

Setelah training selesai, semua hasil (struktur cascade + fitur terpilih + threshold tiap tahap) disimpan dalam format XML.

Isi file tersebut antara lain:

* Ukuran patch (misal 24x24),
* Jumlah stage,
* Daftar fitur Haar terpilih,
* Nilai threshold dan bobot Adaboost,
* Parameter tiap weak classifier.

OpenCV kemudian bisa membaca file ini menggunakan:

```python
cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
```

---

## ⚡ 6. Ringkasan Proses Training Haar Cascade

| Tahap                    | Fungsi                               | Algoritma yang Terlibat |
| ------------------------ | ------------------------------------ | ----------------------- |
| 1. Kumpulkan data        | Siapkan gambar wajah dan bukan wajah | Manual / dataset publik |
| 2. Buat integral image   | Percepat perhitungan kecerahan       | Integral Image          |
| 3. Ekstraksi fitur Haar  | Bentuk pola terang–gelap             | Haar-like features      |
| 4. Seleksi fitur terbaik | Pilih fitur yang paling efektif      | Adaboost                |
| 5. Susun cascade         | Gabungkan fitur dalam tahapan        | Cascade Classifier      |
| 6. Simpan hasil          | Buat file `.xml`                     | OpenCV Training Output  |

---

## 💡 Analogi Sederhana

Bayangkan kamu melatih petugas keamanan:

1. Kamu kasih ribuan foto wajah dan bukan wajah.
2. Mereka belajar mengenali ciri khas wajah (mata, hidung, mulut).
3. Kamu pilih petugas yang paling jeli (Adaboost).
4. Mereka dijadikan tim berlapis (Cascade):
   lapisan pertama menyaring cepat, lapisan terakhir memeriksa dengan cermat.
5. Hasilnya: sistem keamanan yang cepat dan akurat mengenali wajah orang.
