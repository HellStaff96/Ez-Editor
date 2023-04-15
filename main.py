from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog,
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)
from PyQt5 import QtGui
from PIL import Image, ImageFilter
import os 
from PyQt5.QtGui import QPixmap

app = QApplication([])
window = QWidget()
window.resize(700 , 500)
window.setWindowTitle('Ez editor')
window.setWindowIcon(QtGui.QIcon('KLI.jpg'))

"""!ІНТЕРФЕЙС ПРОГРАМИ!"""

btn_folder = QPushButton("Папка")
list_files = QListWidget()

main_label = QLabel("зображення")

btn_left = QPushButton('Вліво')
btn_right = QPushButton("Вправо")
btn_mirror = QPushButton("Дзеркало")
btn_sharp = QPushButton("Різкість")
btn_bw = QPushButton("Ч/Б")
btn_blur = QPushButton("Блюр")
col1 = QVBoxLayout()

col1.addWidget(btn_folder)
col1.addWidget(list_files)

col2 = QVBoxLayout()
col2.addWidget(main_label)

row1 = QHBoxLayout()
row1.addWidget(btn_left)
row1.addWidget(btn_right)
row1.addWidget(btn_mirror)
row1.addWidget(btn_sharp)
row1.addWidget(btn_bw)
row1.addWidget(btn_blur)

col2.addLayout(row1)

main_layout = QHBoxLayout()

main_layout.addLayout(col1)
main_layout.addLayout(col2)

window.setLayout(main_layout)
window.show()


"""ФУНКЦІОНАЛ ПРОГРАМИ"""

workdir = '' #шлях до робочої папки


def chooseWorkdir(): # функція функція вибору папки
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions): # функція фільтрування тільки картинок
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def showFileNamesList():
    extensions = ['.jpg', '.png', '.jpeg', '.bmp', '.gif']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    list_files.clear()

    for filename in filenames:
        list_files.addItem(filename)


class ImageProcessor:
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'Modified/'

    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        main_label.hide()
        pixmapimage = QPixmap(path)
        w, h = main_label.width(), main_label.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        main_label.setPixmap(pixmapimage)
        main_label.show()

    def save_Image(self): # збереження картинки в папку
        path = os.path.join(workdir, self.save_dir)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.save_Image()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.save_Image()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
     

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.save_Image()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.save_Image()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_BW(self):
        self.image = self.image.convert("L")
        self.save_Image()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.save_Image()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

workimage = ImageProcessor()

def showChosenImage():
    if list_files.currentRow() >= 0:
        filename = list_files.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workdir, filename)
        workimage.showImage(image_path)


btn_folder.clicked.connect(showFileNamesList)
list_files.currentRowChanged.connect(showChosenImage)

btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_mirror.clicked.connect(workimage.do_flip)
btn_sharp.clicked.connect(workimage.do_sharpen)
btn_bw.clicked.connect(workimage.do_BW)
btn_blur.clicked.connect(workimage.do_blur)






app.exec_()