import asyncio
from api import get_sensors
from collectors.CollectorBase import CollectorBase
from models.SensorModels import Current, WaterLevel, DHT22
from models.SwitchModels import SwitchBase

SENSOR_MODELS = [Current, WaterLevel, DHT22]

class SensorCollector(CollectorBase):
    def _classify_machine_model(self, sensors) -> SwitchBase:
        results = {}
        for sensor in sensors:
            found_automation_model = next(model for model in SENSOR_MODELS if model.get_name() in sensor['name'])
            results[sensor['name']] = found_automation_model(**sensor)
        return results

    def _get_sensors(self):
        sensors = asyncio.run(get_sensors())
        return sorted(sensors, key=lambda k: k['id'])

    def get(self):
        sensors = self._get_sensors()
        models = self._classify_machine_model(sensors)
        return models