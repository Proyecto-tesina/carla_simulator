class LocationStrategy:
    def __init__(self, carousel, car):
        # TODO
        pass


class SpeedSrategy:
    """
    Args:
        car: the car on which the strategy operates
    """
    def __init__(self, car):
        self.car = car
        self.speed_limit = 20

    def is_busy(self):
        return self.car.stats['speed'] > self.speed_limit


class DistanceStrategy:
    """
    Args:
        car: the car on which the strategy operates
    """
    def __init__(self, car):
        self.car = car
        self.distance_allowed_in_meters = 10

    def is_busy(self):
        nearby_vehicles = self.car.stats['vehicles']
        if nearby_vehicles:
            sorted_vehicles = sorted(nearby_vehicles, key=lambda x: x[0])
            nearest_car_distance = sorted_vehicles[0][0]
            return nearest_car_distance < self.distance_allowed_in_meters
