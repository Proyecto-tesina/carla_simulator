from PySide2.QtWidgets import QLabel
from PySide2.QtCore import Slot, Qt, QFileSystemWatcher, QObject, Signal
from PySide2.QtGui import QPixmap
import json


class FifoStrategy:
    """
    Args:
        carousel: the carousel on which the strategy operates
    """
    def __init__(self, carousel):
        self.carousel = carousel
        self.pos = -1

    def next_image(self):
        self.pos += 1
        if self.pos > len(self.carousel.images_to_roll) - 1:
            self.pos = 0
        return self.pos

    def prev_image(self):
        self.pos -= 1
        if self.pos < 0:
            self.pos = len(self.carousel.images_to_roll) - 1
        return self.pos


class LocationStrategy:
    def __init__(self, carousel, car):
        # TODO
        pass


class SpeedSrategy:
    """
    Args:
        car: the car on which the strategy operates
    """
    def __init__(self, car):
        self.car = car
        self.speed_limit = 20

    def is_busy(self):
        return self.car.stats['speed'] > self.speed_limit


class DistanceStrategy:
    """
    Args:
        car: the car on which the strategy operates
    """
    def __init__(self, car):
        self.car = car
        self.distance_allowed_in_meters = 10

    def is_busy(self):
        nearby_vehicles = self.car.stats['vehicles']
        if nearby_vehicles:
            sorted_vehicles = sorted(nearby_vehicles, key=lambda x: x[0])
            nearest_car_distance = sorted_vehicles[0][0]
            return nearest_car_distance < self.distance_allowed_in_meters


class Carousel:
    """
    Args:
        images: Expects a Python list containing the paths of the images to display.
        strategy: A strategy to show images
    """
    def __init__(self, images=None, strategy=FifoStrategy):
        self.IMAGE_WIDTH = 800
        self.IMAGE_HEIGHT = 600
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
        self.images_to_roll.remove(self.current_image)
        self.next_image()

    def set_show_strategy(self, strategy):
        self.strategy = strategy(self)


class Car(QObject):
    """
    Args:
        risk_calc: Class that serves as strategy to calculate risk of the car
    """
    on_risk = Signal()
    on_calm = Signal()

    def __init__(self, risk_calc=SpeedSrategy):
        QObject.__init__(self)
        self.CAR_INFO_PATH = '../CARLA_simulator/PythonAPI/examples/informacion_del_auto.json'
        self.risk_calc = risk_calc(self)
        self.stats = self._get_car_data()

        self.fs_watcher = QFileSystemWatcher()
        self.fs_watcher.addPath(self.CAR_INFO_PATH)
        self.fs_watcher.fileChanged.connect(self.file_changed)

    def _get_car_data(self):
        try:
            with open(self.CAR_INFO_PATH, 'r', encoding='utf-8') as stats_file:
                stats_data = json.load(stats_file)
            return stats_data
        except (ValueError, UnboundLocalError):
            pass

    def set_risk_calculator(self, risk_calc):
        self.risk_calc = risk_calc(self)

    def file_changed(self):
        self.update_car_stats()
        if self.is_busy():
            self.on_risk.emit()
        else:
            self.on_calm.emit()

    def is_busy(self):
        return self.risk_calc.is_busy()

    def update_car_stats(self):
        stats_data = self._get_car_data()
        if stats_data is not None:
            self.stats = stats_data
