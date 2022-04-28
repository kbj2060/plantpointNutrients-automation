import time
from models.SwitchModels import SwitchBase
from models.managers.DeviceManager import DeviceManager


class LedManager(DeviceManager):
    def __init__(self) -> None:
        DeviceManager.__init__(self)
        self.machine_name = 'led'
        self.sw: SwitchBase = SwitchBase(**(self.select_machines(machine=self.machine_name)[0]))
        self.last_automation = self.select_led_automation()
        self.topic = self.make_machine_topic(self.machine_name)
        self.state = self.select_current_state(self.machine_name)
        self.status = self.state['status']

    def check_condition(self):
        current_time = time.strftime('%H:%M:%S', time.localtime(time.time()))
        return self.last_automation['start'] <= current_time < self.last_automation['end']