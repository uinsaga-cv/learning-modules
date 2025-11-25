# Face Recognition OpenCV (Dataset → Training → Testing)

daftar isi:

1. Membuat Dataset Wajah,
2. Load Dataset & Training Model,
3. Test Recognize dari Gambar,
4. **Test Recognize dari Video**.

---

## 1. MEMBUAT DATASET WAJAH (Face Dataset Collection)

Dataset adalah kumpulan foto wajah yang sudah dicrop dan disimpan di folder per orang.

### 1.1 Struktur Folder Dataset

```bash
dataset/
 ├── person_1/
 │    ├── 0.jpg
 │    ├── 1.jpg
 │    └── ...
 ├── person_2/
 │    ├── 0.jpg
 │    ├── 1.jpg
 │    └── ...
```

### 1.2 Script: Capture & Extract Face dari Webcam

```python
import cv2
import os

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
cam = cv2.VideoCapture(0)

person_name = "person_name"
save_dir = f"dataset/{person_name}"
os.makedirs(save_dir, exist_ok=True)

count = 0

while True:
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for x, y, w, h in faces:
        face = gray[y : y + h, x : x + w]
        face = cv2.resize(face, (200, 200))
        cv2.imwrite(f"{save_dir}/{count}.jpg", face)
        count += 1
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Capture", frame)

    if cv2.waitKey(1) == ord("q") or count >= 50:
        break

cam.release()
cv2.destroyAllWindows()
```

Hasilnya → 50 foto wajah user1.

Lakukan untuk orang lain dengan mengubah `person_name`.

---

## 2. LOAD DATASET & TRAIN FACE RECOGNITION MODEL

Untuk pengenalan wajah (recognition), kita menggunakan:

✔ LBPH Face Recognizer (stabil, cepat, offline)
⚠️ Pastikan sudah install:

```bash
pip install opencv-contrib-python
```

### 2.1 Training Script

```python
import cv2
import os
import numpy as np


def load_dataset(dataset_path="dataset"):
    faces = []
    labels = []
    label_ids = {}  # untuk mapping label → nama orang
    current_label = 0

    for person_name in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, person_name)

        # skip file
        if not os.path.isdir(person_path):
            continue

        label_ids[current_label] = person_name

        for img_name in os.listdir(person_path):
            img_path = os.path.join(person_path, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            if img is None:
                continue

            faces.append(img)
            labels.append(current_label)

        current_label += 1

    return faces, labels, label_ids


faces, labels, label_ids = load_dataset("dataset")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(faces, np.array(labels))

recognizer.save("face_model.xml")

# simpan mapping label → nama
import json

with open("labels.json", "w") as f:
    json.dump(label_ids, f)

print("selesai")
```

Output training:

- `face_model.yml` → model pengenal wajah
- `labels.json` → pemetaan id → nama orang

---

## 3. TEST RECOGNIZE DARI GAMBAR (IMAGE TESTING)

### 3.1 Script Pengujian dari Foto

```python
import cv2
import json

# load model + label
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("face_model.xml")

with open("labels.json", "r") as f:
    label_ids = json.load(f)

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

img = cv2.imread("image.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, 1.3, 5)

for x, y, w, h in faces:
    face_roi = gray[y : y + h, x : x + w]
    label, confidence = recognizer.predict(face_roi)

    name = label_ids[str(label)]
    text = f"{name} ({confidence:.1f})"

    cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

cv2.imshow("Result", img)
cv2.waitKey(5000)

```

---

## 4. TEST RECOGNIZE DARI VIDEO / WEBCAM

### 4.1 Recognizer Real-time Webcam

```python
import cv2
import os
import json

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("face_model.xml")

with open("labels.json", "r") as f:
    label_ids = json.load(f)

# Load Haar Cascade
xmlPath = os.path.join(".", "haarcascade_frontalface_default.xml")
face_cascade = cv2.CascadeClassifier(xmlPath)


# Buka webcam (0 = default camera)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Konversi ke grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Deteksi wajah
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )

    # Gambar kotak pada wajah
    for x, y, w, h in faces:
        face_roi = gray[y : y + h, x : x + w]
        label, confidence = recognizer.predict(face_roi)

        name = label_ids[str(label)]
        text = f"{name} ({confidence:.1f})"

        cv2.putText(
            frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2
        )
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Tampilkan output
    cv2.imshow("Face recognition", frame)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

```

---

## RANGKUMAN

| Bagian                     | Fungsi                                       |
| -------------------------- | -------------------------------------------- |
| 1. Dataset Creation        | Mengambil wajah dari webcam dan menyimpannya |
| 2. Training (Load Dataset) | Melatih model LBPH                           |
| 3. Test Image              | Mengecek model analisis wajah pada gambar    |
| 4. Test Video              | Real-time face recognition dari webcam       |
