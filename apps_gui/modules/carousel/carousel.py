from PySide2.QtWidgets import QLabel
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Slot, Qt
from .strategies import FifoStrategy


class Carousel:
    """
    Args:
        images: Expects a Python list containing the paths of the images to display.
        strategy: A strategy to show images
    """
    def __init__(self, images=None, strategy=FifoStrategy, width=800, height=600):
        self.IMAGE_WIDTH = width
        self.IMAGE_HEIGHT = height
        self.strategy = strategy(self)
        self.images_to_roll = images
        self.current_image = ''

        self.poster = QLabel()
        self.pixmap = QPixmap()
        self.next_image()

    @Slot()
    def next_image(self):
        position = self.strategy.next_image()
        self._render_image_on_pos(position)

    @Slot()
    def prev_image(self):
        position = self.strategy.prev_image()
        self._render_image_on_pos(position)

    def _render_image_on_pos(self, position):
        if not self.images_to_roll:
            self.poster.setText('Lo sentimos, no posee más publicidades guardadas')
            self.poster.setAlignment(Qt.AlignCenter)
        else:
            self.current_image = self.images_to_roll[position]
            self.pixmap.swap(self.current_image)
            self.poster.setPixmap(self.pixmap.scaled(self.IMAGE_WIDTH, self.IMAGE_HEIGHT))

    def delete_current_image(self):
        if self.images_to_roll:
            self.images_to_roll.remove(self.current_image)
            self.next_image()

    def set_strategy(self, strategy):
        self.strategy = strategy(self)
