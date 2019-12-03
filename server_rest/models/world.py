from models import world


class World:
    def __init__(self):
        self.world = world

    def dict(self):
        info = {
                'map': self.world.get_map().name,
                'actors': self.world.get_actors().__str__(),
                'weather': self.world.get_weather().__str__()
        }
        return info
