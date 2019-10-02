import glob
import os
import sys
import math

try:
    sys.path.append(glob.glob('../CARLA_simulator/PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

client = carla.Client('127.0.0.1', 2000)
client.set_timeout(2.0)
world = client.get_world()


class Actor:
    def __init__(self, name):
        actors = world.get_actors()
        self.hero_name = name
        try:
            self.get_player_info(next(filter(self.has_player_name, actors)))
        except StopIteration:
           pass
        
    def has_player_name(self, actor):
        if 'role_name' in actor.attributes:
            return actor.attributes['role_name'] == self.hero_name

    def get_player_info(self, player):
        velocity = player.get_velocity()
        acceleration = player.get_acceleration()
        transform = player.get_transform()

        self.velocity_in_km = 3.6 * math.sqrt(velocity.x**2 + velocity.y**2 + velocity.z**2)
        self.acceleration_in_km = 3.6 * math.sqrt(acceleration.x**2 + acceleration.y**2 + acceleration.z**2)
        self.location = transform.location
        self.control = player.get_control()

    def dict(self):
        info = {
            'velocity': self.velocity_in_km,
            'acceleration': self.acceleration_in_km,
            'location': {
                'x': self.location.x,
                'y': self.location.y
            },
            'height': self.location.z,
            'control': {
                'throttle': (self.control.throttle, 0.0, 1.0),
                'steer': (self.control.steer, -1.0, 1.0),
                'brake': (self.control.brake, 0.0, 1.0),
                'reverse': (self.control.reverse),
                'hand brake': (self.control.hand_brake),
                'manual': (self.control.manual_gear_shift),
                'gear: %s' % {-1: 'R', 0: 'N'}.get(control.gear, control.gear)
            },
        }
        return info
