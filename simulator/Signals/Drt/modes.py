import logging
import random
import time
from abc import ABC, abstractmethod
from threading import Thread

from .Monitor.monitor import Monitor


class Mode(ABC):
    def __init__(self, drt):
        self.drt = drt
        self.monitor = Monitor()
        self.mode_name = None

    @classmethod
    def build(cls, drt):
        cls.mode_name = drt.config.mode_name()

        if cls.mode_name == "random":
            return RandomMode(drt)
        else:
            return ManualMode(drt)

    def toggle(self):
        if self.drt.is_rendered:
            self.turn_off_light()
        else:
            self.turn_on_light()

    @abstractmethod
    def turn_off_light(self):
        self.monitor.add_turn_off_timestamp()

    @abstractmethod
    def turn_on_light(self):
        self.monitor.add_turn_on_timestamp()


class RandomMode(Mode):
    def __init__(self, drt):
        super(RandomMode, self).__init__(drt)

        self.interval = self.drt.config.interval()
        self.region = self.drt.config.region()

        self.start_timer()

    def turn_off_light(self):
        super().turn_off_light()
        self.drt.turn_off()
        self.start_timer()

    def turn_on_light(self):
        # If you try to turn on light manually when in random mode it will count as mistake
        self.monitor.add_mistake_timestamp()
        logging.info('The light wasn\'t on, be careful!')

    def start_timer(self):
        Thread(target=self._schedule_light).start()

    def _schedule_light(self):
        wait_time = random.randint(*self.interval)
        logging.info(f'Making new shedulling for {wait_time}s')

        time.sleep(wait_time)
        self.drt.turn_on()
        self.monitor.add_turn_on_timestamp()


class ManualMode(Mode):

    def turn_off_light(self):
        super().turn_off_light()
        self.drt.turn_off()

    def turn_on_light(self):
        super().turn_on_light()
        self.drt.turn_on()
