import time
from db import MysqlController
from models.managers.DeviceManager import DeviceManager
from models.managers.EnvironmentManager import EnvironmentManager


class ACManager(DeviceManager, MysqlController):
    def __init__(self) -> None:
        DeviceManager.__init__(self)
        MysqlController.__init__(self)
        self.last_automation = self.select_led_automation()
        self.state = self.select_current_state('airconditioner')
        self.status = self.state['status']
        self.topic = self.make_machine_topic('airconditioner')

    def check_condition(self):
        temperature = EnvironmentManager().measure_environment()
        return self.last_automation['start'] <= current_time < self.last_automation['end']