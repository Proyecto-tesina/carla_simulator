from PySide2.QtWidgets import (QAction, QApplication, QMainWindow, QWidget,
                               QPushButton, QVBoxLayout, QHBoxLayout)
from PySide2.QtCore import Slot
from models import Carousel, Car
import sys
import glob
import json


class Publicity_view(QWidget):
    """
    Args:
        window: the main window on which the view operates
    """
    def __init__(self, window):
        QWidget.__init__(self)
        self.saved_images_file = './saved_images.json'
        self.carousel = Carousel(glob.glob('./images/*'))

        self.btn_save = QPushButton('Guardar')
        self.btn_reject = QPushButton('Rechazar')
        self.btn_save.setStyleSheet('background-color: green; color: white')
        self.btn_reject.setStyleSheet('background-color: red; color: white')

        self.options = QHBoxLayout()
        self.options.addWidget(self.btn_reject)
        self.options.addWidget(self.btn_save)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.carousel.poster)
        self.layout.addLayout(self.options)
        self.setLayout(self.layout)

        self.btn_reject.clicked.connect(self.carousel.next_image)
        self.btn_save.clicked.connect(self.save_publicity)

        self.window = window
        try:
            self.window.disconnect_on_calm_signal()
        except (AttributeError, RuntimeError):
            pass

    @Slot()
    def save_publicity(self):
        saved_images = self._get_my_publicity()

        if self.carousel.current_image not in saved_images:
            saved_images.append(self.carousel.current_image)
            with open(self.saved_images_file, 'w', encoding='utf-8') as f:
                json.dump(saved_images, f)

        self.carousel.next_image()

    def _get_my_publicity(self):
        try:
            with open(self.saved_images_file, 'r', encoding='utf-8') as f:
                saved_images = json.load(f)
        except (FileNotFoundError, ValueError):
            saved_images = []
        return saved_images


class Galery_view(QWidget):
    """
    Args:
        window: the main window on which the view operates
    """
    def __init__(self, window):
        QWidget.__init__(self)
        self.saved_images_file = './saved_images.json'
        self.carousel = Carousel(self._get_my_publicity())

        self.btn_delete = QPushButton('Eliminar Publicidad')
        self.btn_delete.setStyleSheet('background-color: red; color: white')

        self.left_arrow = QPushButton('Anterior')
        self.left_arrow.setStyleSheet('background-color: #192c6f; color: white')

        self.right_arrow = QPushButton('Siguiente')
        self.right_arrow.setStyleSheet('background-color: #192c6f; color: white')

        self.controls = QHBoxLayout()
        self.controls.addWidget(self.btn_delete)
        self.controls.addWidget(self.left_arrow)
        self.controls.addWidget(self.right_arrow)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.carousel.poster)
        self.layout.addLayout(self.controls)
        self.setLayout(self.layout)

        self.left_arrow.clicked.connect(self.carousel.prev_image)
        self.right_arrow.clicked.connect(self.carousel.next_image)
        self.btn_delete.clicked.connect(self.delete_publicity)

    @Slot()
    def delete_publicity(self):
        saved_images = self._get_my_publicity()
        saved_images.remove(self.carousel.current_image)
        with open(self.saved_images_file, 'w', encoding='utf-8') as f:
            json.dump(saved_images, f)
        self.carousel.delete_current_image()

    def _get_my_publicity(self):
        try:
            with open(self.saved_images_file, 'r', encoding='utf-8') as f:
                saved_images = json.load(f)
        except (FileNotFoundError, ValueError):
            saved_images = []
        return saved_images


class Map_view(QWidget):
    """
    Args:
        window: the main window on which the view operates
    """
    def __init__(self, window):
        QWidget.__init__(self)
        self.window = window
        self.window.connect_on_calm_signal()

        self.carousel = Carousel(['./map/mapa_La_Plata.png'])

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.carousel.poster)
        self.setLayout(self.layout)


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('Publicidad')
        self.setCentralWidget(Publicity_view(self))

        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu('Acciones')

        exit_action = QAction('Salir', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.exit_app)

        new_publicity = QAction('Publicidades nuevas!', self)

        # Connect expects a function without parameters so I pass a lambda
        new_publicity.triggered.connect(lambda: self.cambiar_vista(Publicity_view))

        my_publicity = QAction('Mis publicidades', self)
        my_publicity.triggered.connect(lambda: self.cambiar_vista(Galery_view))

        self.file_menu.addAction(new_publicity)
        self.file_menu.addAction(my_publicity)
        self.file_menu.addAction(exit_action)

        self.car = Car()
        self.car.on_risk.connect(lambda: self.cambiar_vista(Map_view))

    @Slot()
    def exit_app(self, checked):
        QApplication.quit()

    @Slot()
    def cambiar_vista(self, widget):
        self.setCentralWidget(widget(self))

    def connect_on_calm_signal(self):
        self.car.on_calm.connect(lambda: self.cambiar_vista(Publicity_view))

    def disconnect_on_calm_signal(self):
        self.car.on_calm.disconnect()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec_())
