import random

from .points import RandomPoint, ManualPoint


class Quadrant():

    ROWS = 3
    COLS = 3

    def __init__(self, number, width, height):
        self.number = number
        self.width = width / self.COLS
        self.height = height / self.ROWS

    def x_coords(self):
        return self.start_x(), self.end_x()

    def y_coords(self):
        return self.start_y(), self.end_y()

    def start_x(self):
        return self.width * self.offset_x()

    def offset_x(self):
        return (self.number - 1) % self.COLS

    def end_x(self):
        return self.start_x() + self.width

    def start_y(self):
        return self.height * self.offset_y()

    def offset_y(self):
        return (self.number - 1) // self.COLS

    def end_y(self):
        return self.start_y() + self.height


class Position():
    def __init__(self, drt, width, height):
        self.drt = drt
        self.width, self.height = width, height

    @classmethod
    def build(cls, drt, width, height):
        config = drt.config.position_name()
        position = RandomPosition if config == "random" else FixedPosition
        return position(drt, width, height)

    def refresh(self):
        pass


class FixedPosition(Position):
    def __init__(self, drt, width, height):
        super(FixedPosition, self).__init__(drt, width, height)

        self.x = ManualPoint(0, width, drt.size)
        self.y = ManualPoint(0, height, drt.size)
        self.resolution = self.x.coord(), self.y.coord()


class RandomPosition(Position):

    def __init__(self, drt, width, height):
        super(RandomPosition, self).__init__(drt, width, height)

        self.size = drt.size
        self.quadrants = self.drt.config.quadrants()

        self.refresh()

    def refresh(self):
        quadrant_number = random.choice(self.quadrants)
        quadrant = Quadrant(quadrant_number, self.width, self.height)

        self.x = RandomPoint(*quadrant.x_coords(), self.size)
        self.y = RandomPoint(*quadrant.y_coords(), self.size)

        self.resolution = self.x.coord(), self.y.coord()
