from api import get_last_automation_date, post_automation_history
from collectors.SensorCollector import SensorCollector
from models.Manager import EnvironmentManager, ManagerBase, WaterManager, SprayManager
from collectors.AutomationCollector import AutomationCollector
from collectors.SwitchCollector import SwitchCollector
from datetime import datetime
import RPi.GPIO as GPIO


if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    print(f"DATE: {datetime.now()}")
    print("양액 자동화 시스템 시작합니다.")
    last_spray_activated = get_last_automation_date()['start']
    try:
        automation_models = AutomationCollector().get()
        switch_models = SwitchCollector().get()
        sensor_models = SensorCollector().get()

        em = EnvironmentManager(sensor_models)
        em.measure_environment()

        start = datetime.now()
        wm = WaterManager(switch_models, automation_models, sensor_models)
        wm.control()
        end = datetime.now()
        post_automation_history(subject='watersupply', start=start, end=end, success=True)

        start = datetime.now()
        sm = SprayManager(switch_models, automation_models, sensor_models)
        sm.control(last_spray_activated)
        end = datetime.now()
        post_automation_history(subject='spray', start=start, end=end, success=True)
        
    except:
        now = datetime.now()
        post_automation_history(subject='spray', start=now, end=now, success=True)
    finally:
        GPIO.cleanup()