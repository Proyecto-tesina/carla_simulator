import logging
from abc import ABC, abstractmethod
from datetime import datetime


class DRTState(ABC):
    last_time_on = None

    def __init__(self, drt):
        self.drt = drt
        self.monitor = drt.monitor

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
        logging.info('Discarded USER interaction - Light is already on')

    def turn_on_by_timer(self):
        logging.info('Discarded TIMER interaction - Light is already on')

    def turn_off_by_user(self):
        self._turn_off()
        self.monitor.add_turn_off_timestamp()
        logging.info('Turned light off by USER')

    def turn_off_by_timer(self):
        self._turn_off()
        self.monitor.add_light_lost_timestamp()
        logging.info('Turned light off by TIMER')

    def render(self, display):
        self.drt.show_light(display)


class Off(DRTState):

    def turn_on_by_user(self):
        self._turn_on()
        logging.info('Turned light on by USER')

    def turn_on_by_timer(self):
        self._turn_on()
        logging.info('Turned light on by TIMER')

    def turn_off_by_user(self):
        self.monitor.add_mistake_timestamp()
        logging.info('Light is off - Mistake added')

    def turn_off_by_timer(self):
        logging.info('Discarded TIMER interaction - Light is already off')
