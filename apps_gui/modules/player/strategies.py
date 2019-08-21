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
        self.distance_limit = distance

    def is_busy(self):
        nearest_vehicle = self._get_nearby_vehicles()
        if nearest_vehicle:
            return nearest_vehicle < self.distance_limit

    def _get_nearby_vehicles(self):
        vehicles = self.player.get_world().get_actors().filter('vehicle.*')
        if len(vehicles) > 1:
            distance_to_vehicles = self._get_distances(vehicles)
            return min(distance_to_vehicles)

    def _get_distances(self, vehicles):
        transform = self.player.get_transform()
        dists = []
        for x in vehicles:
            if x.id != self.player.id:
                dists.append(self._distance_between_vehicles(x.get_location(), transform))
        return dists

    def _distance_between_vehicles(self, vehicle1, vehicle2):
        dist = math.sqrt((vehicle1.x - vehicle2.location.x)**2 +
                         (vehicle1.y - vehicle2.location.y)**2 +
                         (vehicle1.z - vehicle2.location.z)**2)
        return dist


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
