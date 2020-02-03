import pygame


class AlertLight(object):
    def __init__(self, size, width, height):
        self.size = size
        self.pos = (width - size - 10, size + 10)
        self._render = False

    def toggle(self):
        self._render = not self._render

    def render(self, display):
        if self._render:
            pygame.draw.circle(display, (235, 64, 52), self.pos, self.size)
