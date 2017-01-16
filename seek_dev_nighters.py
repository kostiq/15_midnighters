import requests
from pytz import timezone
import pytz
from datetime import datetime as dt


def load_attempts():
    api_url = 'https://devman.org/api/challenges/solution_attempts/'
    payload = {'page': '1'}
    pages = requests.get(api_url, params=payload).json()['number_of_pages']
    for page in range(1, pages):
        api_data = requests.get(api_url, params=payload).json()
        payload = {'page': page}
        yield api_data['records']


def filter_midnighters(users_list):
    return list(filter(get_midnight, users_list))


def get_midnight(record):
    fmt = '%H'
    if record['timestamp']:
        tzone = timezone(record['timezone'])
        sending_time = dt.fromtimestamp(float(record['timestamp']))
        local_time = tzone.localize(sending_time)
        hour = int(local_time.strftime(fmt))
        if hour > 0 and hour < 6:
            return True
    else:
        return False


def get_set_midnighters(records):
    owl_set = set()
    for owl in records:
        owl_set.add(owl['username'])
    return owl_set


def print_midnighters(owl_set):
    for user in owl_set:
        print ('{} is owl!'.format(user))


if __name__ == '__main__':
    for page in load_attempts():
        print_midnighters(get_set_midnighters(filter_midnighters(page)))
