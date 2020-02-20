from .timer import TimerOn, TimerOff

from threading import Lock

from abc import ABC

import logging


class Mode(ABC):

    state_lock = Lock()

    @classmethod
    def build(cls, drt):
        mode_name = drt.config.mode_name()

        if mode_name == "random":
            return RandomMode(drt)
        else:
            return ManualMode(drt)

    def __init__(self, drt):
        self.drt = drt
        self.timer_off = TimerOff

    def turn_off_by_user(self):
        self.state_lock.acquire()

        self.drt.state.turn_off_by_user()

        self.state_lock.release()

    def turn_off_by_timer(self, timer):
        self.state_lock.acquire()

        if self.not_turned_on(timer):
            self.drt.state.turn_off_by_timer()
        else:
            logging.info('Discard TIMER')

        self.state_lock.release()

    def not_turned_on(self, timer):
        return self.drt.is_last_time_on(timer.last_time_on)

    def light_on(self):
        self.timer_off(self.drt).start()


class RandomMode(Mode):
    def __init__(self, drt):
        super(RandomMode, self).__init__(drt)

        self.timer_on = TimerOn

    def turn_on_by_user(self):
        logging.info('Invalid "ON by USER" option in Random Mode')

    def turn_on_by_timer(self):
        self.drt.state.turn_on_by_timer()

    def light_off(self):
        self.timer_on(self.drt).start()


class ManualMode(Mode):

    def turn_on_by_user(self):
        self.drt.state.turn_on_by_user()

    def turn_on_by_timer(self):
        logging.info('Invalid "ON by TIMER" option in Manual Mode')

    def light_off(self):
        pass
