import asyncio
from api import get_sensors
from collectors.CollectorBase import CollectorBase
from models.SensorModels import WaterLevel, DHT22


class SensorCollector(CollectorBase):
    def _classify_machine_model(self, sensors):
        results = []
        for sensor in sensors:
            name = sensor['name']
            if 'waterlevel' in name:
                tmp = WaterLevel(**sensor)
            elif 'dht' in name:
                tmp = DHT22(**sensor)
            else:
                raise Exception('해당되는 센서가 존재하지 않습니다.')
            results.append(tmp)
        return results

    def _get_sensors(self):
        return self.select_sensor()

    def get(self):
        sensors = self._get_sensors()
        models = self._classify_machine_model(sensors)
        return models
