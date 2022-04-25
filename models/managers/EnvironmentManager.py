from models.managers.ManagerBase import ManagerBase


class EnvironmentManager(ManagerBase):
    def __init__(self, sensors: dict) -> None:
        self.sensors = sensors

    def measure_environment(self):
        dht = self._find_sensor('dht22')
        dht.post_humidity_temperature()