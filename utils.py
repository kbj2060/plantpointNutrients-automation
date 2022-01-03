from datetime import datetime
import time
from halo import Halo

def fDBDate(date: str):
    return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')

def get_arr_diffs(a, b):
    return list(set(a) - set(b))

def sleep_with_text(waiting_time, text):
    spinner = Halo(text=text, spinner='dots')
    spinner.start()
    time.sleep(waiting_time)
    spinner.stop()