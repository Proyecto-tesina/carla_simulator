from abc import ABC, abstractproperty

from threading import Thread

import random

import time

import logging


class Timer(ABC):

    def __init__(self, mode):
        self.thread = Thread(target=self.switch_light)
        self.drt = mode.drt
        self.mode = mode
        self.render_lock = mode.render_lock

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
        self.last_time_on = self.drt.last_time_on
        logging.info(f'Started scheduler light off {self.duration}s')

    def _end_sleep(self):
        self.render_lock.acquire()

        if self.drt.is_rendered and self.not_turned_on():
            self.mode.turn_off_light()
            logging.info('Light off by Timer')
        else:
            logging.info('Discard timer')

        self.render_lock.release()

    def not_turned_on(self):
        return self.last_time_on == self.drt.last_time_on


class TimerOn(Timer):

    @property
    def duration(self):
        return random.randint(*self.mode.interval)

    def _init_sleep(self):
        logging.info(f'Making new shedulling for {self.duration}s')

    def _end_sleep(self):
        self.mode.turn_on_light()
