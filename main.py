import os
from PIL import Image, ImageFilter
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QLabel,
                             QPushButton,
                             QVBoxLayout,
                             QHBoxLayout,
                             QListWidget,
                             QFileDialog)

app = QApplication([])

app.setWindowIcon(QtGui.QIcon('logo.ico'))


class EditImage(QWidget):
    def __init__(self):
        super().__init__()
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "C:\\Users\\1982m\\Pictures\\python_img"
        self.setup_window()
        self.init_ut()
        self.connect()
        self.show()
        
    def setup_window(self):
        self.setWindowIcon(QtGui.QIcon('logo.ico'))
        self.resize(700, 500)
        self.setWindowTitle("Фото редактор")

    def init_ut(self):
        self.list_foto = QListWidget()
        self.show_foto = QLabel("Картинка")

        self.file_button = QPushButton("Папка")
        self.left_button = QPushButton("Лево")
        self.right_button = QPushButton("Право")
        self.mirrored_button = QPushButton("Зеркало")
        self.blur_button = QPushButton("Резкость")
        self.bluck_white_button = QPushButton("Ч/Б")

        self.support_layout_1 = QVBoxLayout()
        self.support_layout_2 = QVBoxLayout()
        self.button_layout = QHBoxLayout()
        self.main_layout = QHBoxLayout()

        #layout1
        self.support_layout_1.addWidget(self.file_button)
        self.support_layout_1.addWidget(self.list_foto)

        #layout2        
        self.support_layout_2.addWidget(self.show_foto)

        #layout3
        self.button_layout.addWidget(self.left_button)
        self.button_layout.addWidget(self.right_button)
        self.button_layout.addWidget(self.mirrored_button)
        self.button_layout.addWidget(self.blur_button)
        self.button_layout.addWidget(self.bluck_white_button)
        
        #add_layout
        self.support_layout_2.addLayout(self.button_layout)
        self.main_layout.addLayout(self.support_layout_1, 20)
        self.main_layout.addLayout(self.support_layout_2, 80)

        self.setLayout(self.main_layout)

    def choose_workdir(self):
        self.workdir = QFileDialog.getExistingDirectory()

    def foto_filter(self, files, extensions):
        foto_name = []
        for file_name in files:
            for ext in extensions:
                if file_name.endswith(ext):
                    foto_name.append(file_name)
        return foto_name
        
    def show_file_name_list(self):
        self.choose_workdir()
        self.exceptions = [".png", ".jpg", ".jpeg", ".gif", ".bmp"]
        self.file_names = self.foto_filter(os.listdir(self.workdir), self.exceptions)
        self.list_foto.clear()
        for file in self.file_names:
            self.list_foto.addItem(file)

    def load_image(self, dir, filename):
        self.dir = dir
        self.filename = filename
        img_path = os.path.join(self.dir, self.filename)
        self.image = Image.open(img_path)

    def show_image(self, path):
        self.show_foto.hide()
        pixmap_image = QPixmap(path)
        w, h = self.show_foto.width(), self.show_foto.height()
        pixmap_image = pixmap_image.scaled(w, h, Qt.KeepAspectRatio)
        self.show_foto.setPixmap(pixmap_image)
        self.show_foto.show()

    def save_foto(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def show_chosen_image(self):
        if self.list_foto.currentRow() >= 0:
            file_name = self.list_foto.currentItem().text()
            self.load_image(self.workdir, file_name)
            image_path = os.path.join(self.dir, self.filename)
            self.show_image(image_path)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.save_foto()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.save_foto()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.save_foto()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(image_path)

    def do_left_right(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.save_foto()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(image_path)

    def do_blur_foto(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.save_foto()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(image_path)

    def connect(self):
        self.file_button.clicked.connect(self.show_file_name_list)
        self.list_foto.currentRowChanged.connect(self.show_chosen_image)
        self.bluck_white_button.clicked.connect(self.do_bw)
        self.left_button.clicked.connect(self.do_left)
        self.right_button.clicked.connect(self.do_right)
        self.mirrored_button.clicked.connect(self.do_left_right)
        self.blur_button.clicked.connect(self.do_blur_foto)


window = EditImage()
app.exec_()