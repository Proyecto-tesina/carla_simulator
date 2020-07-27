import requests as rq
from datetime import datetime


class Monitor:
    def __init__(self):
        self.URL = 'http://127.0.0.1:8000/events/drt/'

    def add_turn_on_timestamp(self):
        self.post_event('start')

    def add_mistake_timestamp(self):
        self.post_event('mistake')

    def add_light_lost_timestamp(self):
        self.post_event('lost')

    def add_turn_off_timestamp(self):
        self.post_event('end')

    def post_event(self, status):
        body = {
            'timestamp': datetime.now().isoformat(),
            'status': status,
        }
        rq.post(self.URL, data=body)
