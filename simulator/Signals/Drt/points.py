import random


class Point():

    MARGIN = 10

    def __init__(self, min_value, max_value, size):
        self.max_value = int(max_value)
        self.min_value = int(min_value)
        self.__init_size(size)

    def __init_size(self, size):
        max_radius = (self.max_value - self.min_value) / 2

        if size <= max_radius:
            self.size = size
        else:
            error_msg = f'Size of DRT light should be less to {max_radius}px.'
            raise Exception(error_msg)

    def calculate_position(self, value):
        if self.is_outside_display(value):
            return self.offset(value)
        else:
            return value

    def is_outside_display(self, value):
        return self.is_minor_offset(value) or self.is_max_offset(value)

    def is_minor_offset(self, value):
        return value - self.size < self.min_value

    def is_max_offset(self, value):
        return value + self.size > self.max_value

    def offset(self, value):
        if self.is_minor_offset(value):
            return value + self.size + self.MARGIN
        elif self.is_max_offset(value):
            return value - self.size - self.MARGIN


class RandomPoint(Point):

    def coord(self):
        random_value = random.randint(self.min_value, self.max_value)
        return self.calculate_position(random_value)


class ManualPoint(Point):

    def __init__(self, min_value, max_value, coord, size):
        super(ManualPoint, self).__init__(min_value, max_value, size)
        self._coord = coord

    def coord(self):
        return self.calculate_position(self._coord)
