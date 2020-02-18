import logging

from .timer import TimerOn, TimerOff

from abc import ABC

from .Monitor.monitor import Monitor

from threading import Lock


class Mode(ABC):
    render_lock = Lock()

    @classmethod
    def build(cls, drt):
        mode_name = drt.config.mode_name()

        if mode_name == "random":
            return RandomMode(drt)
        else:
            return ManualMode(drt)

    def __init__(self, drt):
        self.drt = drt
        self.monitor = Monitor()
        self.timer_off = TimerOff

    def toggle(self):
        """Entry by User event"""
        self.render_lock.acquire()

        if self.drt.is_rendered:
            self.toggle_rendered()
        else:
            self.toggle_not_rendered()

        self.render_lock.release()

    def toggle_rendered(self):
        self.turn_off_light()
        logging.info('Light off by User')

    def turn_off_light(self):
        self.drt.turn_off()
        self.monitor.add_turn_off_timestamp()

    def turn_on_light(self):
        self.drt.turn_on()
        self.monitor.add_turn_on_timestamp()
        self.timer_off(self).start()


class RandomMode(Mode):
    def __init__(self, drt):
        super(RandomMode, self).__init__(drt)

        self.interval = self.drt.config.interval()
        self.region = self.drt.config.region()
        self.timer_on = TimerOn

        self.timer_on(self).start()

    def turn_off_light(self):
        super().turn_off_light()
        self.timer_on(self).start()

    def toggle_not_rendered(self):
        # If you try to turn on light manually when
        # in random mode it will count as mistake
        self.monitor.add_mistake_timestamp()
        logging.info('The light wasn\'t on, be careful!')


class ManualMode(Mode):

    def toggle_not_rendered(self):
        self.turn_on_light()
