import pygame

from .config import DRTConfiguration
from .modes import Mode
from .positions import Position
from .state import On, Off


class AlertLight(object):

    def __init__(self, width, height):
        self.config = DRTConfiguration()

        self.duration = self.config.duration()
        self.interval = self.config.interval()
        self.size = self.config.size()
        self.color = pygame.Color(self.config.color())

        self.mode = Mode.build(self)
        self.position = Position.build(self, width, height)

        self.set_off_state()

    # Switch states

    def set_on_state(self):
        self.state = On(self)
        self.position.refresh()
        self.mode.light_on()

    def set_off_state(self):
        self.state = Off(self)
        self.mode.light_off()

    # Renders

    def show_light(self, display):
        pygame.draw.circle(
            display,
            self.color,
            self.position.resolution,
            self.size
        )

    def render(self, display):
        self.state.render(display)

    # Entrys for actors:

    def turn_on_by_user(self):
        self.mode.turn_on_by_user()

    def turn_on_by_timer(self):
        self.mode.turn_on_by_timer()

    def turn_off_by_user(self):
        self.mode.turn_off_by_user()

    def turn_off_by_timer(self, timer):
        self.mode.turn_off_by_timer(timer)

    # Querys

    def is_last_time_on(self, last_time):
        return self.state.is_last_time_on(last_time)

    def last_time_on(self):
        return self.state.last_time_on
