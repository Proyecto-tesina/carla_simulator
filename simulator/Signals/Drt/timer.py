from abc import ABC, abstractproperty

from threading import Thread

import random

import time

import logging


class Timer(ABC):

    def __init__(self, drt):
        self.thread = Thread(target=self.switch_light)
        self.drt = drt

    def start(self):
        self.thread.start()

    def switch_light(self):
        self._init_sleep()
        time.sleep(self.duration)
        self._end_sleep()

    def _init_sleep(self):
        pass

    @abstractproperty
    def duration(self):
        pass

    def _end_sleep(self):
        pass


class TimerOff(Timer):

    @property
    def duration(self):
        return self.drt.duration

    def _init_sleep(self):
        self.last_time_on = self.drt.last_time_on()
        logging.info(f'Started scheduler light OFF in {self.duration}s')

    def _end_sleep(self):
        self.drt.turn_off_by_timer(self)


class TimerOn(Timer):

    @property
    def duration(self):
        return random.randint(*self.mode.interval)

    def _init_sleep(self):
        logging.info(f'Started scheduler light ON in {self.duration}s')

    def _end_sleep(self):
        self.drt.turn_on_by_timer()
