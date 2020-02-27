from datetime import datetime


class AlertTimeLine:
    def __init__(self):
        self.turn_on_time = datetime.now()
        self.turn_off_time = None
        self.light_lost_time = None
        self.mistakes = []

    def serialize_data(self):
        return {
            'turn_on_time': self.get_turn_on_time_formated(),
            'turn_off_time': self.get_turn_off_time_formated(),
            'light_lost_time': self.get_light_lost_time_formated(),
            'mistakes': self.get_mistakes_formated(),
            'response_time': self.get_response_time(),
        }

    def set_turn_off_time(self):
        self.turn_off_time = datetime.now()

    def set_light_lost_time(self):
        self.light_lost_time = datetime.now()

    def get_light_lost_time_formated(self):
        if self.light_lost_time:
            return self.light_lost_time.isoformat()

    def get_turn_off_time_formated(self):
        if self.turn_off_time:
            return self.turn_off_time.isoformat()

    def get_turn_on_time_formated(self):
        return self.turn_on_time.isoformat()

    def add_mistake(self):
        self.mistakes.append(datetime.now())

    def get_mistakes_formated(self):
        return list(map(lambda mistake: mistake.isoformat(), self.mistakes))

    def get_response_time(self):
        """ Returns the time between the end and start of timeline represented in miliseconds """
        end_time = self.turn_off_time if self.turn_off_time else self.light_lost_time
        response_time = end_time - self.turn_on_time
        return response_time.microseconds / 1000

    def get_cant_mistakes(self):
        return len(self.mistakes)
