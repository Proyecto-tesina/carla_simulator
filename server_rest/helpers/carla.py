import math


def get_actor_display_name(actor, truncate=250):
    name = ' '.join(actor.type_id.replace('_', '.').title().split('.')[1:])
    return (name[:truncate - 1] + u'\u2026') if len(name) > truncate else name

def distance_between_vehicles(vehicle1, vehicle2):
    dist = math.sqrt((vehicle1.x - vehicle2.location.x)**2 +
                     (vehicle1.y - vehicle2.location.y)**2 +
                     (vehicle1.z - vehicle2.location.z)**2)
    return dist

def convert_to_km(potency):
    return 3.6 * math.sqrt(potency.x**2 + potency.y**2 + potency.z**2)

