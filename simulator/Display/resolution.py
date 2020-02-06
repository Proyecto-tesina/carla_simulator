from abc import ABC, abstractmethod

from screeninfo import screeninfo

import pygame


class Resolution(ABC):

    @abstractmethod
    def width(self):
        pass

    @abstractmethod
    def height(self):
        pass

    @abstractmethod
    def mode(self):
        pass

    def size(self):
        return self.width(), self.height()

    def __str__(self):
        return f'{self.width()}x{self.height()}'


class CustomResolution(Resolution):
    def __init__(self, width, height):
        self.__width, self.__height = width, height

    def width(self):
        return self.__width

    def height(self):
        return self.__height

    def mode(self):
        return pygame.HWSURFACE | pygame.DOUBLEBUF


class MultimonitorResolution(Resolution):
    def __init__(self):
        self.monitors = screeninfo.get_monitors()

    def width(self):
        return sum(self.monitors_width())

    def monitors_width(self):
        return [monitor.width for monitor in self.monitors]

    def height(self):
        return min(self.monitors_height())

    def monitors_height(self):
        return [monitor.height for monitor in self.monitors]

    def mode(self):
        return pygame.FULLSCREEN
