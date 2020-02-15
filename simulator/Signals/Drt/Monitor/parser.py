import json


class MonitorParser:
    def __init__(self, path):
        self.path = path

    def write_to_file(self, timelines):
        data = self.parse_data(timelines)
        with open(self.path, 'w') as file:
            json_str = json.dumps(data, indent=4)
            file.write(json_str)

    def parse_data(self, timelines):
        data = {
            'experiment_run_detail': self.parse_timelines(timelines),
            'average_response': self.get_average_response_time(timelines),
            'total_drt_lights': len(timelines),
            'total_turned_off_lights': self.get_turned_off_lights(timelines),
            'total_lost_lights': self.get_lost_lights(timelines),
            'total_mistakes': self.get_total_mistakes(timelines),
            'average_mistakes': self.get_average_mistakes(timelines),
        }
        return data

    def parse_timelines(self, timeline_objects):
        alert_timelines = []
        for timeline in timeline_objects:
            alert_timelines.append(timeline.serialize_data())
        return alert_timelines

    def get_average_response_time(self, timeline_objects):
        total_time = sum(
            map(lambda obj: obj.get_response_time(), timeline_objects))
        cant_objs = len(timeline_objects)
        return total_time / cant_objs

    def get_turned_off_lights(self, timeline_objects):
        timelines = list(filter(
            lambda obj: obj.turn_off_time, timeline_objects))
        return len(timelines)

    def get_lost_lights(self, timeline_objects):
        timelines = list(filter(
            lambda obj: obj.light_lost_time, timeline_objects))
        return len(timelines)

    def get_total_mistakes(self, timeline_objects):
        return sum(map(lambda obj: obj.get_cant_mistakes(), timeline_objects))

    def get_average_mistakes(self, timeline_objects):
        total_mistakes = self.get_total_mistakes(timeline_objects)
        cant_objs = len(timeline_objects)
        return total_mistakes / cant_objs
