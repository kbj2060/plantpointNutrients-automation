from datetime import datetime
import time
import numpy as np
from halo import Halo

def fDBDate(date: str):
    return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')

def get_arr_diffs(a, b):
    return list(set(a) - set(b))

def sleep_with_text(waiting_time, text):
    spinner = Halo(text=text, spinner='dots')
    spinner.start()
    time.sleep(waiting_time)
    spinner.stop_and_persist()

def detect_outlier(arr):
    outliers=[]
    threshold=3
    mean_1 = np.mean(arr)
    std_1 =np.std(arr)

    for y in arr:
        z_score= (y - mean_1)/std_1 
        if np.abs(z_score) > threshold:
            outliers.append(y)
    return outliers