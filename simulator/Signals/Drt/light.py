import pygame

from .config import DRTConfiguration
from .modes import Mode
from .positions import Position


class AlertLight(object):

    def __init__(self, width, height):
        self.config = DRTConfiguration()

        self.size = self.config.size()
        self.color = pygame.Color(self.config.color())

        self.mode_on = Mode.build(self)
        self.position = Position.build(self, width, height)

        self.is_rendered = False

    def toggle(self):
        self.mode_on.toggle()

    def turn_on(self):
        self.position.refresh()
        self.is_rendered = True

    def turn_off(self):
        self.is_rendered = False

    def render(self, display):
        if self.is_rendered:
            pygame.draw.circle(
                display,
                self.color,
                self.position.resolution,
                self.size
            )
