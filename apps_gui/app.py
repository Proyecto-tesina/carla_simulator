from PySide2.QtWidgets import QAction, QApplication, QMainWindow
from PySide2.QtCore import Slot
from modules.widgets.widgets import PublicityView, GaleryView, MapView
from modules.player.player import PlayerObserver
from modules.player.strategies import WeatherStrategy
import sys
import argparse


class MainWindow(QMainWindow):
    def __init__(self, args):
        QMainWindow.__init__(self)
        self.setWindowTitle('Publicidad')
        self.set_widget_publicity()
        self._create_menu()

        self.player = PlayerObserver(args.name, WeatherStrategy, args.host, args.port)

        self.player.on_calm.connect(self.set_widget_publicity)
        self.player.on_risk.connect(self.set_widget_map)

    def _create_menu(self):
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu('Acciones')

        exit_action = QAction('Salir', self)
        exit_action.setShortcut('Ctrl+Q')

        new_publicity = QAction('Publicidades nuevas!', self)
        my_publicity = QAction('Mis publicidades', self)

        new_publicity.triggered.connect(self.set_widget_publicity)
        my_publicity.triggered.connect(self.set_widget_galery)
        exit_action.triggered.connect(self.exit_app)

        self.file_menu.addAction(new_publicity)
        self.file_menu.addAction(my_publicity)
        self.file_menu.addAction(exit_action)

    @Slot()
    def exit_app(self):
        QApplication.quit()

    @Slot()
    def set_widget_publicity(self):
        self.setCentralWidget(PublicityView())

    @Slot()
    def set_widget_map(self):
        self.setCentralWidget(MapView())

    @Slot()
    def set_widget_galery(self):
        self.setCentralWidget(GaleryView())


def main():
    argparser = argparse.ArgumentParser(description='Main Window of the App')
    argparser.add_argument(
        '--host',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)')
    argparser.add_argument(
        '-p', '--port',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)')
    argparser.add_argument(
        '-n', '--name',
        default='hero',
        help='Player name (default: "hero")')
    args = argparser.parse_args()

    app = QApplication(sys.argv)
    window = MainWindow(args)
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
