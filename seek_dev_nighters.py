import requests
import pytz
from datetime import datetime as dt


def load_attempts():
    pages = 11
    for page in range(1, pages):
        r = requests.get(
            'https://devman.org/api/challenges/solution_attempts/?page='+str(page))
        yield r.json()['records']


def get_midnighters(tasks_to_check):
    return filter(filter_midnight, tasks_to_check)


def filter_midnight(record):
    fmt = '%H'
    if record['timestamp']:
        sending_time = dt.fromtimestamp(float(record['timestamp']))
        hour = int(sending_time.strftime(fmt))
        if hour > 0 and hour < 9:
            return True
    else:
        return False


def print_midnighters(records):
    for user in records:
        print ('{} is owl!'.format(user['username']))


if __name__ == '__main__':
    for page in load_attempts():
        print_midnighters(get_midnighters(page))
