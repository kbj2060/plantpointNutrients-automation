from db import MysqlController
from models.SensorModels import DHT22
from models.managers.DeviceManager import DeviceManager


class ACManager(DeviceManager, MysqlController):
    def __init__(self) -> None:
        DeviceManager.__init__(self)
        MysqlController.__init__(self)
        self.last_automation = self.select_led_automation()
        self.state = self.select_current_state('airconditioner')
        self.status = self.state['status']
        self.topic = self.make_machine_topic('airconditioner')

    def check_condition(self):
        sensor = self.select_sensor('dht22')
        humidity, temperature = DHT22(**sensor).get_values()
        return int(self.last_automation['start']) <= temperature < int(self.last_automation['end'])