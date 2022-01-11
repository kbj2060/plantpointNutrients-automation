import asyncio
from api import get_last_automations, post_automation_history, post_report
from collectors.SensorCollector import SensorCollector
from config import WATERTANK_LIMIT
from models.Manager import EnvironmentManager, WaterManager, SprayManager
from collectors.AutomationCollector import AutomationCollector
from collectors.SwitchCollector import SwitchCollector
from datetime import datetime
import RPi.GPIO as GPIO
from utils import DB_date, str2datetime


class SprayPassException(Exception):
    pass

def check_spray_condition():
    sprayterm = asyncio.run(get_last_automations('sprayterm'))
    spray_last_activated = AutomationCollector.get_last_activated('spray')
    last_term = (datetime.now() - str2datetime(spray_last_activated)).total_seconds()/60
    if round(last_term) >= sprayterm:
        return True

def check_water_condition():
    water_last_activated = AutomationCollector.get_last_activated('watersupply')
    if water_last_activated['isCompleted']:
        return True

def check_waterlevel_condition(waterlevel_sensor):
    waterlevel = waterlevel_sensor.get_waterlevel()
    if waterlevel <= WATERTANK_LIMIT:
        return True


if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    print(f"DATE: {datetime.now()}")
    print("양액 자동화 시스템 시작합니다.")
    
    try:
        sensor_models = SensorCollector().get()

        em = EnvironmentManager(sensor_models)
        em.measure_environment()

        automation_models = AutomationCollector().get()
        switch_models = SwitchCollector().get()

        if check_waterlevel_condition(sensor_models['waterlevel']):
            wm = WaterManager(switch_models, automation_models, sensor_models)
            wm.control()

        if check_spray_condition() and check_water_condition():
            sm = SprayManager(switch_models, automation_models, sensor_models)
            sm.control()

    except SprayPassException:
        print('스프레이 자동화는 작동하지 않는 조건입니다.')

    except:
        print('자동화 시스템이 시스템 에러로 인해 중단되었습니다.')
        now = DB_date(datetime.now())
        asyncio.run(post_automation_history(subject='error', start=now, isCompleted=False))
        asyncio.run(post_report(lv=3, problem='자동화 시스템이 시스템 에러로 인해 중단되었습니다.'))

    finally:
        GPIO.cleanup()
