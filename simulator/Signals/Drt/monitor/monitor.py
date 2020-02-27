from .alert_timeline import AlertTimeLine
from .serializer import MonitorSerializer


class Monitor:
    def __init__(self):
        self.current_timeline = None
        self.alert_timelines = []
        self.parser = MonitorSerializer(path='simulator/monitor_results.json')

    def add_turn_on_timestamp(self):
        self.current_timeline = AlertTimeLine()

    def add_turn_off_timestamp(self):
        self.current_timeline.set_turn_off_time()
        self.alert_timelines.append(self.current_timeline)
        self.parser.write_to_file(self.alert_timelines)

    def add_mistake_timestamp(self):
        self.current_timeline.add_mistake()

    def add_light_lost_timestamp(self):
        self.current_timeline.set_light_lost_time()
        self.alert_timelines.append(self.current_timeline)
        self.write_to_file(self.alert_timelines)
