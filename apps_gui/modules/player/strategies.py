import math


class SpeedSrategy:
    """
    Args:
        player: the player on which the strategy operates
        speed: the velocity in kilometers before the player is busy
    """
    def __init__(self, player, speed=20):
        self.player = player
        self.speed_limit = speed

    def is_busy(self):
        velocity = self.player.get_velocity()
        velocity_in_km = 3.6 * math.sqrt(velocity.x**2 + velocity.y**2 + velocity.z**2)
        return velocity_in_km > self.speed_limit


class DistanceStrategy:
    """
    Args:
        player: the player on which the strategy operates
        distance: the distance in meters to other cars on wich the player is busy
    """
    def __init__(self, player, distance=10):
        self.player = player
        self.distance_allowed = distance

    def is_busy(self):
        nearby_vehicles = self._get_nearby_vehicles()
        if nearby_vehicles:
            return self.nearest_vehicle_distance(nearby_vehicles) < self.distance_allowed

    def _get_nearby_vehicles(self):
        vehicles = self.player.get_world.get_actors().filter('vehicle.*')
        nearby_vehicles = []

        if len(vehicles) > 1:
            distance_vehicle_pairs = self._get_vehicle_distance_pairs(vehicles)
            for distance, vehicle in sorted(distance_vehicle_pairs):
                if distance > 200.0:
                    break
                vehicle_type = self._get_actor_display_name(vehicle, truncate=22)
                nearby_vehicles.append((distance, vehicle_type))
        return nearby_vehicles

    def _get_vehicle_distance_pairs(self, vehicles):
        transform = self.player.get_transform()
        pairs = []
        for x in vehicles:
            if x.id != self.player.id:
                pairs.append((self._distance_between_vehicles(x.get_location(), transform), x))
        return pairs

    def _distance_between_vehicles(self, vehicle1, vehicle2):
        dist = math.sqrt((vehicle1.x - vehicle2.location.x)**2 +
                         (vehicle1.y - vehicle2.location.y)**2 +
                         (vehicle1.z - vehicle2.location.z)**2)
        return dist

    def _get_actor_display_name(actor, truncate=250):
        name = ' '.join(actor.type_id.replace('_', '.').title().split('.')[1:])
        return (name[:truncate - 1] + u'\u2026') if len(name) > truncate else name

    def _nearest_vehicle_distance(self, nearby_vehicles):
        sorted_vehicles = sorted(nearby_vehicles, key=lambda x: x[0])
        return sorted_vehicles[0][0]


class WeatherStrategy:
    """
    Args:
        player: the player on which the strategy operates
        rain_limit: the limit of precipitation before the player is busy
    """
    def __init__(self, player, rain_limit=0):
        self.player = player
        self.rain_limit = rain_limit

    def is_busy(self):
        return self.get_rain_level() > self.rain_limit

    def get_rain_level(self):
        world = self.player.get_world()
        weather = world.get_weather()
        return weather.precipitation
