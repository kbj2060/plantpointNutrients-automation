from models.SensorModels import DHT22
from models.managers.ManagerBase import ManagerBase


class EnvironmentManager(ManagerBase):
    def __init__(self, sensors) -> None:
        self.sensors = sensors

    def measure_and_post(self):
        dht: DHT22 = self._find_sensor('dht22')
        dht.post_values()()