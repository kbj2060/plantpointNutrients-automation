from models.AutoControl import AutoControl
from collectors.AutomationCollector import AutomationCollector
from collectors.SwitchCollector import SwitchCollector

if __name__ == "__main__":
    automation_models = AutomationCollector().get()
    switch_models = SwitchCollector().get()
    autocontrol = AutoControl(switch_models, automation_models)
    autocontrol.control_water()
    autocontrol.control_nutrient()
    # [ s.pprint() for s in automation_models]
    # [ s.pprint() for s in switch_models]
