import math
import threading
import requests as rq
from datetime import datetime


class PlayerMonitor:
    BASE_URL = "http://127.0.0.1:8000"

    def __init__(self):
        self.velocity = 0
        self.steer = 0
        try:
            self.EXPERIMENT_TARGET_ID = rq.get(
                f"{self.BASE_URL}/experiments/last"
            ).json()["id"]
        except rq.exceptions.ConnectionError:
            self.HAS_CONNECTION = False
        else:
            self.HAS_CONNECTION = True

    def tick(self, world, clock):
        player = world.player
        velocity = player.get_velocity()
        control = player.get_control()
        self.check_movement(control.steer, velocity, control.reverse)

    def check_movement(self, steer, velocity, reverse):
        velocity_in_km = round(
            3.6 * math.sqrt(velocity.x ** 2 + velocity.y ** 2 + velocity.z ** 2)
        )
        # Usually the steer is 0 and this minimizes the writes on file
        if steer != self.steer:
            rounded_steer = round(steer, 1)
            if rounded_steer == -0.2:
                self._call_post_thread("Turn left")
            elif rounded_steer == 0.2:
                self._call_post_thread("Turn right")
            elif rounded_steer == 0 and velocity_in_km != 0 and not reverse:
                self._call_post_thread("Moving forward")
            self.steer = steer

        if velocity_in_km != self.velocity:
            if velocity_in_km == 0:
                self._call_post_thread("Stoped")
            elif self.velocity == 10 and reverse and velocity_in_km > self.velocity:
                self._call_post_thread("Moving backwards")
            self.velocity = velocity_in_km

    def _call_post_thread(self, status):
        if self.HAS_CONNECTION:
            threading.Thread(target=self._post_event, args=(status,)).start()

    def _post_event(self, status):
        body = {
            "name": "PLAYER",
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "experiment": self.EXPERIMENT_TARGET_ID,
        }
        rq.post(f"{self.BASE_URL}/events/", data=body)
