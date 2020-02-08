import pygame

from .modes import Mode

from .positions import Position

from .config import DRTConfiguration


class AlertLight(object):

    def __init__(self, width, height):
        self.config = DRTConfiguration()

        self.size = self.config.size()
        self.color = pygame.Color(self.config.color())

        self.mode_on = Mode.build(self)
        self.position = Position.build(self, width, height)

        self.is_render = False

    def toggle(self):
        self.mode_on.toggle()

    def turn_on(self):
        self.position.refresh()
        self.is_render = True

    def turn_off(self):
        self.is_render = False

    def render(self, display):
        if self.is_render:
            pygame.draw.circle(
                display,
                self.color,
                self.position.resolution,
                self.size
            )
