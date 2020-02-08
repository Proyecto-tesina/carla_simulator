import json


class DRTConfiguration():
    PATH = 'simulator/drt_config.json'

    def __init__(self):
        try:

            with open(self.PATH) as config_file:
                data = json.load(config_file)
                self.config = data.get("config")
                self.modes = data.get("modes")
                self.positions = data.get("positions")

        except Exception as e:

            raise e('An error ocurred with config DRT file')

    def size(self):
        return self.config.get('size')

    def color(self):
        return self.config.get('color')

    def mode(self):
        try:
            return list(filter(
                lambda mode: mode.get("id") == self.id_mode(),
                self.modes
            ))[0]
        except IndexError:
            raise IndexError('Invalid mode on config DRT file')

    def mode_name(self):
        return self.mode().get('name')

    def id_mode(self):
        return self.config.get('mode_on')

    def interval(self):
        interval = self.mode().get('interval')
        return tuple(interval.values())

    def position(self):
        try:
            return list(filter(
                lambda position: position.get("id") == self.id_position(),
                self.positions
            ))[0]
        except IndexError:
            raise IndexError('Invalid position on config DRT file')

    def id_position(self):
        return self.config.get('position')

    def random_region(self):
        return self.position().get('region')

    def fixed_coords(self):
        coords = self.position().get('coords')
        return tuple(coords.values())

    def region(self):
        return self.config.get('region')

    def position_name(self):
        return self.position().get('name')
