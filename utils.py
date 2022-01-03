from datetime import datetime
from halo import Halo

def fDBDate(date: str):
    return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')

def get_arr_diffs(a, b):
    return list(set(a) - set(b))

def sleep_with_text(time, text):
    spinner = Halo(text=text, spinner='dots')
    spinner.start()
    time.sleep(time)
    spinner.stop()