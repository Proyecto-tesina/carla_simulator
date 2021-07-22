import threading
import requests as rq
from datetime import datetime


class Monitor:
    BASE_URL = "http://127.0.0.1:8000"

    def __init__(self):
        try:
            self.EXPERIMENT_TARGET_ID = rq.get(
                f"{self.BASE_URL}/experiments/last"
            ).json()["id"]
        except rq.exceptions.ConnectionError:
            self.HAS_CONNECTION = False
        else:
            self.HAS_CONNECTION = True

    def add_turn_on_timestamp(self):
        self._call_post_thread("start")

    def add_mistake_timestamp(self):
        self._call_post_thread("mistake")

    def add_light_lost_timestamp(self):
        self._call_post_thread("lost")

    def add_turn_off_timestamp(self):
        self._call_post_thread("end")

    def _call_post_thread(self, status):
        if self.HAS_CONNECTION:
            threading.Thread(target=self._post_event, args=(status,)).start()

    def _post_event(self, status):
        body = {
            "name": "DRT",
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "experiment": self.EXPERIMENT_TARGET_ID,
        }
        rq.post(f"{self.BASE_URL}/events/", data=body)
