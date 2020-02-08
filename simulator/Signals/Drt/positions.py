import random


class Point():

    MARGIN = 10

    def __init__(self, max_value, size):
        self.max_value = max_value
        self.size = size

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


class RandomPoint(Point):

    def coord(self):
        random_value = random.randrange(self.max_value)
        return self.calculate_position(random_value)


class ManualPoint(Point):

    def coord(self):
        return self.calculate_position(self.max_value)


class Position():
    def __init__(self, drt, width, height, Point):
        self.x = Point(width, drt.size)
        self.y = Point(height, drt.size)
        self.resolution = self.x.coord(), self.y.coord()

    @classmethod
    def build(cls, drt, width, height):
        if drt.config.position_name() == "random":
            return RandomPosition(
                drt,
                width,
                height,
                RandomPoint
            )
        else:
            return cls(
                drt,
                width,
                height,
                ManualPoint
            )

    def refresh(self):
        pass


class RandomPosition(Position):

    def refresh(self):
        self.resolution = self.x.coord(), self.y.coord()
