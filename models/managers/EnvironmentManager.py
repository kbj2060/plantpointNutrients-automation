from models.SensorModels import DHT22
from models.managers.ManagerBase import ManagerBase


class EnvironmentManager(ManagerBase):
    def __init__(self, sensors: dict) -> None:
        self.sensors = sensors

    def measure(self):
        dht: DHT22 = self._find_sensor('dht22')
        humidity, temperature = dht.get_values()
        return humidity, temperature