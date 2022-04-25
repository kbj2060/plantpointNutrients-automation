import time
from models.managers.DeviceManager import DeviceManager


class LedManager(DeviceManager):
    def __init__(self) -> None:
        DeviceManager.__init__(self)
        self.last_automation = self.select_led_automation()
        self.state = self.select_current_state('led')
        self.status = self.state['status']
        self.topic = self.make_machine_topic('led')

    def check_condition(self):
        current_time = time.strftime('%H:%M:%S', time.localtime(time.time()))
        return self.last_automation['start'] <= current_time < self.last_automation['end']