from .Monitor.monitor import Monitor

from abc import ABC, abstractmethod

from datetime import datetime

import logging


class DRTState(ABC):

    monitor = Monitor()
    last_time_on = None

    def __init__(self, drt):
        self.drt = drt

    def _turn_on(self):
        self.drt.set_on_state()
        self.monitor.add_turn_on_timestamp()

    def _turn_off(self):
        self.drt.set_off_state()

    @abstractmethod
    def turn_on_by_user(self):
        pass

    @abstractmethod
    def turn_on_by_timer(self):
        pass

    @abstractmethod
    def turn_off_by_user(self):
        pass

    @abstractmethod
    def turn_off_by_timer(self):
        pass

    def is_last_time_on(self, last_time):
        return self.last_time_on == last_time

    def render(self, display):
        pass


class On(DRTState):

    def __init__(self, drt):
        super(On, self).__init__(drt)
        self.last_time_on = datetime.today()

    def turn_on_by_user(self):
        logging.info('Discard USER - Light ON already')

    def turn_on_by_timer(self):
        logging.info('Discard TIMER - Light ON already')

    def turn_off_by_user(self):
        self._turn_off()
        self.monitor.add_turn_off_timestamp()
        logging.info('Light OFF by USER')

    def turn_off_by_timer(self):
        self._turn_off()
        # self.monitor.add_light_lost_timestamp()
        logging.info('Light OFF by TIMER')

    def render(self, display):
        self.drt.show_light(display)


class Off(DRTState):

    def turn_on_by_user(self):
        self._turn_on()
        logging.info('Light ON by USER')

    def turn_on_by_timer(self):
        self._turn_on()
        logging.info('Light ON by TIMER')

    def turn_off_by_user(self):
        self.monitor.add_mistake_timestamp()
        logging.info('Discard USER - Mistake added')

    def turn_off_by_timer(self):
        logging.info('Discard TIMER')
