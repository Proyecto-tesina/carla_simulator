import pygame
import threading
import time
import random
import logging


class RandomPoint():

    MARGIN = 10

    def __init__(self, max_value, size):
        self.max_value = max_value
        self.size = size

    def new_value(self):
        random_value = random.randrange(self.max_value)
        return self.calculate_position(random_value)

    def calculate_position(self, value):
        if self.is_outside_display(value):
            return self.offset(value)
        else:
            return value

    def is_outside_display(self, value):
        return self.is_minor_offset(value) or self.is_max_offset(value)

    def is_minor_offset(self, value):
        return value - self.size < 0

    def is_max_offset(self, value):
        return value + self.size > self.max_value

    def offset(self, value):
        if self.is_minor_offset(value):
            return value + self.size + self.MARGIN
        elif self.is_max_offset(value):
            return value - self.size - self.MARGIN


class RandomPosition():
    def __init__(self, size, width, height):
        self.random_width = RandomPoint(width, size)
        self.random_height = RandomPoint(height, size)
        self.refresh()

    def refresh(self):
        self.resolution = self.__new_position()

    def __new_position(self):
        return self.random_width.new_value(), self.random_height.new_value()


class AlertLight(object):

    COLOR = (235, 64, 52)

    def __init__(self, size, width, height, pos_refresh=False, interval=None):
        self.size = size
        self.pos = RandomPosition(size, width, height)
        self.interval = interval
        self.pos_refresh_active = pos_refresh
        self._render = False

        if interval:
            self.assert_drt()

    def toggle(self):
        if self._render:
            self.turn_off_light()
        else:
            self.turn_on_light()

    def assert_drt(self):
        if self.interval:
            self.turn_off_light()
            threading.Thread(target=self._schedule_light).start()
        else:
            logging.warning(
                'Cannot schedule DRT light, there\'s no interval specified')

    def _schedule_light(self):
        wait_time = random.randint(self.interval[0], self.interval[1])
        time.sleep(wait_time)
        self.turn_on_light()

    def turn_on_light(self):
        if self.pos_refresh_active:
            self.pos.refresh()
        self._render = True

    def turn_off_light(self):
        self._render = False

    def render(self, display):
        if self._render:
            pygame.draw.circle(
                display,
                self.COLOR,
                self.pos.resolution,
                self.size
            )
