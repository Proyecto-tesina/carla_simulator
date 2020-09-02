import math
import threading
import requests as rq
from datetime import datetime


class PlayerMonitor:
    BASE_URL = 'http://127.0.0.1:8000'

    def __init__(self):
        self.velocity = 0
        self.steer = 0
        self.EXPERIMENT_TARGET_ID = rq.get(
            f'{self.BASE_URL}/experiments/last').json()['id']

    def tick(self, world, clock):
        player = world.player
        velocity = player.get_velocity()
        control = player.get_control()
        self.check_steer_event(control.steer)
        self.check_velocity_event(velocity, control.reverse)

    def check_steer_event(self, steer):
        # Usually the steer is 0 and this minimizes the writes on file
        if steer != self.steer:
            self.steer = steer
            if round(self.steer, 1) == -0.3:
                self._call_post_thread('Turn left')
            elif round(self.steer, 1) == 0.3:
                self._call_post_thread('Turn right')

    def check_velocity_event(self, velocity, reverse):
        velocity_in_km = round(
            3.6 * math.sqrt(velocity.x**2 + velocity.y**2 + velocity.z**2))
        if velocity_in_km != self.velocity:
            if velocity_in_km == 0:
                self._call_post_thread('Stoped')
            elif velocity_in_km == 10 and not reverse and velocity_in_km > self.velocity:
                self._call_post_thread('Moving forward')
            elif self.velocity == 10 and reverse and velocity_in_km > self.velocity:
                self._call_post_thread('Moving backwards')
            self.velocity = velocity_in_km

    def _call_post_thread(self, status):
        threading.Thread(target=self._post_event, args=(status, )).start()

    def _post_event(self, status):
        body = {
            'name': 'PLAYER',
            'timestamp': datetime.now().isoformat(),
            'status': status,
            'experiment': self.EXPERIMENT_TARGET_ID,
        }
        rq.post(f'{self.BASE_URL}/events/', data=body)
