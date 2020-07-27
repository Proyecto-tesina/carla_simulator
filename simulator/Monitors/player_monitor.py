import requests as rq
import math
from datetime import datetime


class Player_Monitor:
    def __init__(self):
        self.URL = 'http://127.0.0.1:8000/events/player/'
        self.velocity = 0
        self.steer = 0
        self.events = []

    def tick(self, world, clock):
        player = world.player
        velocity = player.get_velocity()
        control = player.get_control()

        self.value_changed = False
        self.check_steer_event(control.steer)
        self.check_velocity_event(velocity, control.reverse)
        if self.value_changed:
            self.post_events()

    def check_steer_event(self, steer):
        # Usually the steer is 0 and this minimizes the writes on file
        if steer != self.steer:
            self.steer = steer
            self.value_changed = True
            if round(self.steer, 1) == -0.3:
                self.events.append((datetime.now().isoformat(), 'Turn left'))
            elif round(self.steer, 1) == 0.3:
                self.events.append((datetime.now().isoformat(), 'Turn right'))

    def check_velocity_event(self, velocity, reverse):
        velocity_in_km = round(
            3.6 * math.sqrt(velocity.x**2 + velocity.y**2 + velocity.z**2))
        if velocity_in_km != self.velocity:
            self.value_changed = True
            if velocity_in_km == 0:
                self.events.append(
                    (datetime.now().isoformat(), 'Stoped'))
            elif velocity_in_km == 10 and not reverse and velocity_in_km > self.velocity:
                self.events.append(
                    (datetime.now().isoformat(), 'Moving forward'))
            elif self.velocity == 10 and reverse and velocity_in_km > self.velocity:
                self.events.append(
                    (datetime.now().isoformat(), 'Moving backwards'))
            self.velocity = velocity_in_km

    def post_events(self):
        for event in self.events:
            body = {
                'timestamp': event[0],
                'status': event[1],
            }
            rq.post(self.URL, data=body)
        self.events.clear()
