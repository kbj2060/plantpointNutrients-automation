from db import MysqlController
from models.SensorModels import DHT22
from models.SwitchModels import SwitchBase
from models.managers.DeviceManager import DeviceManager


class ACManager(DeviceManager):
    def __init__(self) -> None:
        DeviceManager.__init__(self)
        self.machine_name = 'airconditioner'
        self.sw: SwitchBase = SwitchBase(**(self.select_machines(machine=self.machine_name)[0]))
        self.last_automation = self.select_ac_automation()
        self.state = self.select_current_state(self.machine_name)
        self.status = self.state['status']
        self.topic = self.make_machine_topic(self.machine_name)

    def check_condition(self):
        # sensor = self.select_sensor('dht22')
        # humidity, temperature = DHT22(**sensor).get_values()
        temperature = int(self.select_last_temperature()['value'])
        return int(self.last_automation['start']) <= temperature < int(self.last_automation['end'])