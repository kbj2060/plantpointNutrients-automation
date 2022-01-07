from datetime import datetime
import time
import numpy as np
from halo import Halo

def fDBDate(date: str):
    return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')

def get_arr_diffs(a, b):
    return list(set(a) - set(b))

# def sleep_with_log(waiting_time, text):
#     spinner = Halo(text=text, spinner='dots', text_color='yellow')
#     spinner.start()
#     time.sleep(waiting_time)
#     spinner.stop_and_persist()

def turn_on_log(text):
    spinner = Halo(spinner='dots', text_color='green')
    spinner.succeed(text=text)

def turn_off_log(text):
    spinner = Halo(spinner='dots', text_color='red')
    spinner.succeed(text=text)

def detect_outlier(arr):
    outliers=[]
    threshold=1
    mean_1 = np.mean(arr)
    std_1 =np.std(arr)
    if std_1 == 0: return []
    for y in arr:
        z_score = (y - mean_1) / std_1
        if np.abs(z_score) > threshold:
            outliers.append(y)
    return outliers

def DB_date(date: datetime):
    return date.strftime('%Y-%m-%d %H:%M:%S')

def str2datetime(date):
    return date.strptime('%Y-%m-%d %H:%M:%S')