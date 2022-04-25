import time
from db import MysqlController
from models.managers.DeviceManager import DeviceManager


MIN_HOUR = 0
MAX_HOUR = 23

class RoofFanManager(DeviceManager, MysqlController):
    def __init__(self) -> None:
        DeviceManager.__init__(self)
        MysqlController.__init__(self)
        self.last_automation = self.select_rooffan_automation()
        self.topic = self.make_machine_topic('rooffan')
        self.state = self.select_current_state('rooffan')
        self.status = self.state['status']
        self.term = self.last_automation['term']

    def check_condition(self):
        current_hour = int(time.strftime('%H', time.localtime(time.time())))
        right_hours = [ h for h in range(MIN_HOUR, MAX_HOUR + 1) if h // self.term % 2 == 0 ]
        return current_hour in right_hours