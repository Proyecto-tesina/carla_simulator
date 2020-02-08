import random

import time

from threading import Thread

from abc import ABC, abstractmethod


class Mode(ABC):
    def __init__(self, drt):
        self.drt = drt

    @classmethod
    def build(self, drt):
        if drt.config.mode_name() == "random":
            return RandomMode(drt)
        else:
            return ManualMode(drt)

    @abstractmethod
    def toggle(self):
        pass


class RandomMode(Mode):
    def __init__(self, drt):
        super(RandomMode, self).__init__(drt)

        self.interval = self.drt.config.interval()
        self.region = self.drt.config.region()

        self.start_timer()

    def toggle(self):
        if self.drt.is_render:
            self.turn_off()

    def turn_off(self):
        self.drt.turn_off()
        self.start_timer()

    def start_timer(self):
        Thread(target=self._schedule_light).start()

    def _schedule_light(self):
        wait_time = random.randint(*self.interval)
        print('New shedulling on:', wait_time)

        time.sleep(wait_time)
        self.drt.turn_on()


class ManualMode(Mode):

    def toggle(self):
        if self.drt.is_render:
            self.drt.turn_off()
        else:
            self.drt.turn_on()
