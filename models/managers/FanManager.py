import time
from config import MAX_HOUR, MIN_HOUR
from models.SwitchModels import Fan, SwitchBase
from models.managers.DeviceManager import DeviceManager

class FanManager(DeviceManager):
    def __init__(self) -> None:
        DeviceManager.__init__(self)
        self.machine_name = 'fan'
        self.sw: SwitchBase = SwitchBase(**(self.select_machines(machine=self.machine_name)[0]))
        self.last_automation = self.select_fan_automation()
        self.topic = self.make_machine_topic(self.machine_name)
        self.state = self.select_current_state(self.machine_name)
        self.status = self.state['status']
        self.term = self.last_automation['term']

    def check_condition(self):
        current_hour = int(time.strftime('%H', time.localtime(time.time())))
        right_hours = [ h for h in range(MIN_HOUR, MAX_HOUR+1) if h // self.term % 2 == 0 ]
        return current_hour in right_hours