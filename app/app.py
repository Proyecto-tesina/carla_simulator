from PySide2.QtWidgets import QAction, QApplication, QMainWindow
from PySide2.QtCore import Slot
from modules.widgets.widgets import PublicityView, GaleryView, MapView
from modules.player.player import PlayerObserver
import sys
import argparse


class MainWindow(QMainWindow):
    def __init__(self, args):
        QMainWindow.__init__(self)
        self.setWindowTitle('Publicidad')
        self.set_publicity_widget()
        self._create_menu()

        self.player = PlayerObserver(player=args.name, host=args.host, port=args.port)

        self.player.on_calm.connect(self.set_publicity_widget)
        self.player.on_risk.connect(self.set_map_widget)

    def _create_menu(self):
        self.menu = self.menuBar()
        self.app_menu = self.menu.addMenu('Acciones')

        exit_action = QAction('Salir', self)
        exit_action.setShortcut('Ctrl+Q')

        new_publicity = QAction('Publicidades nuevas!', self)
        my_publicity = QAction('Mis publicidades', self)

        new_publicity.triggered.connect(self.set_publicity_widget)
        my_publicity.triggered.connect(self.set_galery_widget)
        exit_action.triggered.connect(self.exit_app)

        self.app_menu.addAction(new_publicity)
        self.app_menu.addAction(my_publicity)
        self.app_menu.addAction(exit_action)

    @Slot()
    def exit_app(self):
        QApplication.quit()

    @Slot()
    def set_publicity_widget(self):
        self.setCentralWidget(PublicityView())

    @Slot()
    def set_map_widget(self):
        self.setCentralWidget(MapView())

    @Slot()
    def set_galery_widget(self):
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
