from collectors.SensorCollector import SensorCollector
from models.AutoControl import AutoControl
from collectors.AutomationCollector import AutomationCollector
from collectors.SwitchCollector import SwitchCollector

if __name__ == "__main__":
    automation_models = AutomationCollector().get()
    switch_models = SwitchCollector().get()
    sensor_models = SensorCollector().get()

    autocontrol = AutoControl(switch_models, automation_models, sensor_models)
    autocontrol.control_water()
    autocontrol.control_spray()
