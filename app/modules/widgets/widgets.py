from PySide2.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PySide2.QtCore import Slot
from modules.carousel.carousel import Carousel
import glob
import json


class PublicityView(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.saved_images_file = './data/saved_images.json'

        carousel_images = glob.glob('./images/*')
        self.carousel = Carousel(carousel_images)

        self._create_buttons()
        self._create_layout()

    def _create_buttons(self):
        self.btn_save = QPushButton('Guardar')
        self.btn_save.setStyleSheet('background-color: green; color: white')

        self.btn_reject = QPushButton('Rechazar')
        self.btn_reject.setStyleSheet('background-color: red; color: white')

        self.btn_reject.clicked.connect(self.carousel.next_image)
        self.btn_save.clicked.connect(self.save_publicity)

    def _create_layout(self):
        self.options = QHBoxLayout()
        self.options.addWidget(self.btn_reject)
        self.options.addWidget(self.btn_save)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.carousel.poster)
        self.layout.addLayout(self.options)
        self.setLayout(self.layout)

    @Slot()
    def save_publicity(self):
        saved_images = self._get_my_publicity()

        if self.carousel.current_image not in saved_images:
            saved_images.append(self.carousel.current_image)
            with open(self.saved_images_file, 'w+', encoding='utf-8') as f:
                json.dump(saved_images, f)

        self.carousel.next_image()

    def _get_my_publicity(self):
        try:
            with open(self.saved_images_file, 'r', encoding='utf-8') as f:
                saved_images = json.load(f)
        except (FileNotFoundError, ValueError):
            saved_images = []
        return saved_images


class GaleryView(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.saved_images_file = './data/saved_images.json'

        carousel_images = self._get_my_publicity()
        self.carousel = Carousel(carousel_images)

        self._create_buttons()
        self._create_layout()

    def _create_buttons(self):
        self.btn_delete = QPushButton('Eliminar Publicidad')
        self.btn_delete.setStyleSheet('background-color: red; color: white')

        self.left_arrow = QPushButton('Anterior')
        self.left_arrow.setStyleSheet('background-color: #192c6f; color: white')

        self.right_arrow = QPushButton('Siguiente')
        self.right_arrow.setStyleSheet('background-color: #192c6f; color: white')

        self.left_arrow.clicked.connect(self.carousel.prev_image)
        self.right_arrow.clicked.connect(self.carousel.next_image)
        self.btn_delete.clicked.connect(self.delete_publicity)

    def _create_layout(self):
        self.controls = QHBoxLayout()
        self.controls.addWidget(self.btn_delete)
        self.controls.addWidget(self.left_arrow)
        self.controls.addWidget(self.right_arrow)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.carousel.poster)
        self.layout.addLayout(self.controls)
        self.setLayout(self.layout)

    @Slot()
    def delete_publicity(self):
        self._delete_publicity_from_file()
        self.carousel.delete_current_image()

    def _delete_publicity_from_file(self):
        """ Removes the current publicity from user's file of saved publicities """
        saved_images = self._get_my_publicity()
        if saved_images:
            saved_images.remove(self.carousel.current_image)
        with open(self.saved_images_file, 'w', encoding='utf-8') as f:
            json.dump(saved_images, f)

    def _get_my_publicity(self):
        try:
            with open(self.saved_images_file, 'r', encoding='utf-8') as f:
                saved_images = json.load(f)
        except (FileNotFoundError, ValueError):
            saved_images = []
        return saved_images


class MapView(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.carousel = Carousel(['./map/mapa_La_Plata.png'])
        self._create_layout()

    def _create_layout(self):
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.carousel.poster)
        self.setLayout(self.layout)
