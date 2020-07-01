import json
from datetime import datetime

try:
    with open('./simulator/monitor_results.json', 'r') as file:
        results = json.load(file)
except FileNotFoundError as error:
    print('Couldn\'t retrieve file with monitor results')
    raise error


def parse_results(results):
    info = {
        'start': [],
        'end': [],
        'lost': [],
        'mistake': [],
    }

    def parse_string(event):
        time = event[0]
        return datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%f')

    for event in results:
        time_object = parse_string(event)
        info[event[1]].append(time_object)

    return info


def calculate_response_times(start_events, end_events):
    response_times = []

    for index, event in enumerate(end_events):
        response = event - start_events[index]
        response_in_miliseconds = response.microseconds / 1000

        response_times.append(response_in_miliseconds)
    return response_times


def calculate_average(items):
    return sum(items) / len(items)


parsed_results = parse_results(results)
response_times = calculate_response_times(
    parsed_results['start'], parsed_results['end'])


computed_results = {
    'start_events': len(parsed_results['start']),
    'end_events': len(parsed_results['end']),
    'lost_events': len(parsed_results['lost']),
    'mistake_events': len(parsed_results['mistake']),
    'average_response_time (ms)': calculate_average(response_times),
}

print(json.dumps(computed_results, indent=4))
