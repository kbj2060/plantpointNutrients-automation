import asyncio
from api import get_last_automations, post_automation_history, post_report
from collectors.AutomationCollector import AutomationCollector
from collectors.SensorCollector import SensorCollector
from collectors.SwitchCollector import SwitchCollector

from datetime import datetime
from logger import logger
from models.Mqtt import MQTT
from models.managers.ACManager import ACManager
from models.managers.EnvironmentManager import EnvironmentManager
from models.managers.FanManager import FanManager
from models.managers.LedManager import LedManager
from models.managers.RoofFanManager import RoofFanManager
from models.managers.SprayManager import SprayManager
from models.managers.WaterManager import WaterManager
import RPi.GPIO as GPIO
from utils import DB_date
from entities.error import WaterException


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

def control_machines():
    managers = [FanManager, RoofFanManager, ACManager, LedManager]
    for manager in managers:
        asyncio.run(manager().control())

if __name__ == "__main__":
    try:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        logger.info(f"DATE: {datetime.now()}")
        logger.info("양액 자동화 시스템 시작합니다.")

        control_machines()

        am = AutomationCollector().get()
        sw = SwitchCollector().get()
        ss = SensorCollector().get()

        em = EnvironmentManager(ss)
        em.measure_and_post()

        wm = WaterManager(switches=sw, automations=am, sensors=ss)
        wm.control()

        sm = SprayManager(switches=sw, automations=am, sensors=ss)
        sm.control()

    except WaterException as e:
        problem = e.args[0]
        asyncio.run(post_report(lv=3, problem=problem))
        print(e)
    except:
        logger.error('자동화 시스템이 알 수 없는 에러로 인해 중단되었습니다.')
        asyncio.run(post_automation_history(subject='spray', createdAt=DB_date(datetime.now()), isCompleted=False))
        asyncio.run(post_automation_history(subject='water', createdAt=DB_date(datetime.now()), isCompleted=False))
        asyncio.run(post_report(lv=3, problem='자동화 시스템이 알 수 없는 에러로 인해 중단되었습니다.'))
    finally:
        GPIO.cleanup()
        print("GPIO clean up!")
        MQTT().client.disconnect()
