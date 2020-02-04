from helpers.carla import get_actor_display_name, distance_between_locations, convert_to_km
from models import world


class Actor:
    def __init__(self, name):
        self.actors = world.get_actors()
        self.hero_name = name
        try:
            self.player = next(filter(self.has_player_name, self.actors))
        except StopIteration:
            raise Exception('Player not found')
        self.init_player_info(self.player)

    def has_player_name(self, actor):
        if 'role_name' in actor.attributes:
            return actor.attributes['role_name'] == self.hero_name

    def init_player_info(self, player):
        velocity = player.get_velocity()
        acceleration = player.get_acceleration()

        self.velocity_in_km = convert_to_km(velocity)
        self.acceleration_in_km = convert_to_km(acceleration)
        self.transform = player.get_transform()
        self.location = self.transform.location
        self.control = player.get_control()

    def get_nearby_vehicles(self):
        vehicles = self.actors.filter('vehicle.*')
        if len(vehicles) > 1:
            dist_vehicle_pair = self._get_pair(vehicles)
            return dist_vehicle_pair

    def _get_pair(self, vehicles):
        """ Return the pair (distance, vehicle_name) of a vehicles list or an empty list """
        pairs = []
        for x in vehicles:
            if x.id != self.player.id:
                vehicle_info = (distance_between_locations(x.get_location(), self.transform),
                                get_actor_display_name(x))
                pairs.append(vehicle_info)
        return pairs

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
                'reverse': (self.control.reverse),
                'hand brake': (self.control.hand_brake),
                'manual': (self.control.manual_gear_shift),
                'gear': {-1: 'R', 0: 'N'}.get(self.control.gear,
                                              self.control.gear),
            },
            'nearby-vehicles': self.get_nearby_vehicles(),
        }
        return info