import json
from datetime import datetime


class Monitor:
    def __init__(self):
        self.events = []
        self.path = 'simulator/monitor_results.json'

    def add_turn_on_timestamp(self):
        event = (datetime.now().isoformat(), 'start')
        self.events.append(event)

    def add_mistake_timestamp(self):
        event = (datetime.now().isoformat(), 'mistake')
        self.events.append(event)

    def add_light_lost_timestamp(self):
        event = (datetime.now().isoformat(), 'lost')
        self.events.append(event)
        self.write_to_file(self.events)

    def add_turn_off_timestamp(self):
        event = (datetime.now().isoformat(), 'end')
        self.events.append(event)
        self.write_to_file(self.events)

    def write_to_file(self, events):
        with open(self.path, 'w') as file:
            json_str = json.dumps(events, indent=4)
            file.write(json_str)
