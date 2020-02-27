import json


class ConfigParser():
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

    def light_on_duration(self):
        return self.config.get('light_on_duration')

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
        return self.config.get('mode_id')

    def light_off_interval(self):
        interval = self.mode().get('light_off_interval')
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

    def quadrants(self):
        if any(self.chosen_quadrants()):
            return list(
                map(int, self.chosen_quadrants())
            )
        else:
            raise Exception('You must choose at least one quadrant')

    def chosen_quadrants(self):
        quadrants = self.position().get('quadrants')
        return [number for number, chosen in quadrants.items() if chosen]
