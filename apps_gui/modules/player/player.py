from PySide2.QtCore import QObject, Signal
from .strategies import SpeedSrategy
import glob
import sys

try:
    sys.path.append(glob.glob('../CARLA_simulator/PythonAPI/carla/dist/*')[0])
except IndexError as e:
    raise e

import carla


class PlayerObserver(QObject):
    """
    Args:
        risk_calc: Class that serves as strategy to calculate risk of the car
    """
    on_risk = Signal()
    on_calm = Signal()

    def __init__(self, player='hero', risk_calc=SpeedSrategy, host='127.0.0.1', port=2000):
        QObject.__init__(self)
        world = self._get_world_of_client(host, port)
        actors = world.get_actors()

        self.player_name = player
        self.player = self._get_player_from_actors(actors)

        self.last_signal = None

        self.risk_calc = risk_calc(self.player)
        world.on_tick(self.check_risk)

    def _get_world_of_client(self, host, port):
        client = carla.Client(host, port)
        client.set_timeout(2.0)
        return client.get_world()

    def _get_player_from_actors(self, actors):
        player = filter(self._has_player_name, actors)
        try:
            return next(player)
        except StopIteration as e:
            print('\nThere isn\'t a player called "{}" between the actors\n' .format(self.player_name))
            raise e

    def _has_player_name(self, actor):
        if 'role_name' in actor.attributes:
            return actor.attributes['role_name'] == self.player_name

    def set_player_name(self, name):
        self.player_name = name

    def set_risk_calculator(self, risk_calc):
        self.risk_calc = risk_calc(self.player)

    def check_risk(self, timestamp):
        if self.is_busy():
            self.emit_on_risk()
        else:
            self.emit_on_calm()

    def is_busy(self):
        return self.risk_calc.is_busy()

    def emit_on_risk(self):
        if self.last_signal != 'on_risk':
            self.last_signal = 'on_risk'
            self.on_risk.emit()

    def emit_on_calm(self):
        if self.last_signal != 'on_calm':
            self.last_signal = 'on_calm'
            self.on_calm.emit()
