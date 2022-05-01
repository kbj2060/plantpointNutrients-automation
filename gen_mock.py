import csv
import os
from datetime import datetime, timedelta
from random import randrange



def get_midnight_date (date):
    return datetime(date.year, date.month, date.day, 0, 0, 0)


def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta


def get_result(start, end):
    return [[None, randrange(start, end), dt.strftime('%Y-%m-%d %H:%M')]
            for index, dt in
            enumerate(datetime_range(get_midnight_date(today), get_midnight_date(tomorrow), timedelta(minutes=5)))]


if __name__ == '__main__':
    today = datetime.today()
    tomorrow = datetime.today() + timedelta(days=1)
    ranges = {
        'temp': { 'start': 23, 'end': 30 },
        'hum': { 'start': 45, 'end': 55 }
    }
    for sub in ['temp', 'hum']:
        if os.path.isfile(f"./{sub}.csv"):
            os.remove(f"./{sub}.csv")
        with open(f"{sub}.csv", "a+") as my_csv:
            csvWriter = csv.writer(my_csv, delimiter=',')
            csvWriter.writerows(get_result(start=ranges[sub]['start'], end=ranges[sub]['end']))