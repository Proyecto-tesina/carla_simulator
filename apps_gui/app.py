from PySide2.QtWidgets import QAction, QApplication, QMainWindow
from PySide2.QtCore import Slot
from modules.car.car import Car
from modules.widgets.widgets import PublicityView, GaleryView, MapView
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('Publicidad')
        self.setCentralWidget(PublicityView(self))

        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu('Acciones')

        exit_action = QAction('Salir', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.exit_app)

        new_publicity = QAction('Publicidades nuevas!', self)

        # Connect expects a function without parameters so I pass a lambda
        new_publicity.triggered.connect(lambda: self.cambiar_vista(PublicityView))

        my_publicity = QAction('Mis publicidades', self)
        my_publicity.triggered.connect(lambda: self.cambiar_vista(GaleryView))

        self.file_menu.addAction(new_publicity)
        self.file_menu.addAction(my_publicity)
        self.file_menu.addAction(exit_action)

        car_info_path = '../CARLA_simulator/PythonAPI/examples/informacion_del_auto.json'
        self.car = Car(car_info_path)
        self.car.on_risk.connect(lambda: self.cambiar_vista(MapView))

    @Slot()
    def exit_app(self, checked):
        QApplication.quit()

    @Slot()
    def cambiar_vista(self, widget):
        self.setCentralWidget(widget(self))

    def connect_on_calm_signal(self):
        self.car.on_calm.connect(lambda: self.cambiar_vista(PublicityView))

    def disconnect_on_calm_signal(self):
        self.car.on_calm.disconnect()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec_())
