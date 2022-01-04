from collectors.SensorCollector import SensorCollector
from models.Manager import EnvironmentManager, WaterManager, SprayManager
from collectors.AutomationCollector import AutomationCollector
from collectors.SwitchCollector import SwitchCollector
from datetime import datetime
import RPi.GPIO as GPIO

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    print(f"DATE: {datetime.now()}")
    print("양액 자동화 시스템 시작합니다.")
    automation_models = AutomationCollector().get()
    switch_models = SwitchCollector().get()
    sensor_models = SensorCollector().get()

    em = EnvironmentManager(sensor_models)
    em.measure_environment()

    wm = WaterManager(switch_models, automation_models, sensor_models)
    wm.control()

    sm = SprayManager(switch_models, automation_models, sensor_models)
    sm.control()
    
    GPIO.cleanup()