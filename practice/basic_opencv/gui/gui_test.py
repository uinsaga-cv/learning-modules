import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QFileDialog,
)
from PyQt5.QtGui import QPixmap, QImage


class ImageApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikasi Pengolahan Citra - OpenCV")
        self.image = None

        # Komponen UI
        self.label = QLabel("Belum ada gambar", self)
        self.btn_load = QPushButton("Muat Gambar", self)
        self.btn_gray = QPushButton("Ubah ke Grayscale", self)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btn_load)
        layout.addWidget(self.btn_gray)
        self.setLayout(layout)

        # Event handler
        self.btn_load.clicked.connect(self.load_image)
        self.btn_gray.clicked.connect(self.to_gray)

    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Pilih Gambar", "", "Image Files (*.png *.jpg *.jpeg)"
        )
        if path:
            self.image = cv2.imread(path)
            self.display_image(self.image)

    def to_gray(self):
        if self.image is not None:
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.display_image(gray, is_gray=True)

    def display_image(self, img, is_gray=False):
        if is_gray:
            qformat = QImage.Format_Grayscale8
            h, w = img.shape
            bytes_per_line = w
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            h, w, ch = img.shape
            bytes_per_line = ch * w
            qformat = QImage.Format_RGB888

        qimg = QImage(img.data, w, h, bytes_per_line, qformat)
        self.label.setPixmap(QPixmap.fromImage(qimg).scaled(500, 400))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageApp()
    window.resize(600, 500)
    window.show()
    sys.exit(app.exec_())
