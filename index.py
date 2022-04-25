import asyncio
from api import get_last_automations, post_automation_history, post_report
# from collectors.SensorCollector import SensorCollector
from config import WATERTANK_LIMIT
# from models.Manager import EnvironmentManager, WaterManager, SprayManager
# from collectors.AutomationCollector import AutomationCollector
# from collectors.SwitchCollector import SwitchCollector
from datetime import datetime
from db import MysqlController
from models.managers.FanManager import FanManager
from models.managers.RoofFanManager import RoofFanManager
# import RPi.GPIO as GPIO
from utils import DB_date, str2datetime


class SprayPassException(Exception):
    pass

# def check_spray_condition():
#     sprayterm = asyncio.run(get_last_automations('sprayterm'))['period']
#     spray_last_activated = AutomationCollector.get_last_activated('spray')['createdAt']
#     print(f"마지막 작동 시간은 {spray_last_activated} 입니다.")
#     last_term = (datetime.now() - str2datetime(spray_last_activated)).total_seconds()/60
#     if round(last_term) >= sprayterm:
#         return True

# def check_water_condition():
#     water_last_activated = AutomationCollector.get_last_activated('watersupply', isCompleted= True)
#     if water_last_activated['isCompleted']:
#         return True

# def check_waterlevel_condition(waterlevel_sensor):
#     if not waterlevel_sensor.get_waterlevel():
#         return True

if __name__ == "__main__":
    l = RoofFanManager()
    print(l.control())

    # GPIO.setwarnings(False)
    # GPIO.setmode(GPIO.BCM)
    # print(f"DATE: {datetime.now()}")
    # print("양액 자동화 시스템 시작합니다.")
    
    # sensor_models = SensorCollector().get()

    # em = EnvironmentManager(sensor_models)
    # em.measure_environment()


    # automation_models = AutomationCollector().get()
    # switch_models = SwitchCollector().get()

    # if check_waterlevel_condition(sensor_models['lower_waterlevel']):
    #     wm = WaterManager(switch_models, automation_models, sensor_models)
    #     wm.control()
    # else: print("수급 작동 조건이 충족되지 않았습니다.")

    # if check_spray_condition() and check_water_condition():
    #     sm = SprayManager(switch_models, automation_models, sensor_models)
    #     sm.control()
    # else: print("스프레이 작동 조건이 충족되지 않았습니다.")
    
    # print('자동화 시스템이 시스템 에러로 인해 중단되었습니다.')
    # now = DB_date(datetime.now())
    # asyncio.run(post_automation_history(subject='error', createdAt=now, isCompleted=False))
    # asyncio.run(post_report(lv=3, problem='자동화 시스템이 시스템 에러로 인해 중단되었습니다.'))
    
    # GPIO.cleanup()
