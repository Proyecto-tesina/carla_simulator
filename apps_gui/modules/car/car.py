from PySide2.QtCore import QObject, Signal, QFileSystemWatcher
from .strategies import SpeedSrategy
import json


class Car(QObject):
    """
    Args:
        risk_calc: Class that serves as strategy to calculate risk of the car
    """
    on_risk = Signal()
    on_calm = Signal()

    def __init__(self, car_info_path, risk_calc=SpeedSrategy):
        QObject.__init__(self)
        self.CAR_INFO_PATH = car_info_path
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
