import asyncio
from api import get_sensors
from collectors.CollectorBase import CollectorBase
from models.SensorModels import Current, SensorModel, WaterLevel, DHT22
from models.SwitchModels import SwitchBase


class SensorCollector(CollectorBase):
    def _classify_machine_model(self, sensors):
        # results = {}
        # for sensor in sensors:
        #     found_automation_model = next(model for model in SENSOR_MODELS if model.get_name() in sensor['name'])
        #     results[sensor['name']] = found_automation_model(**sensor)
        # return results
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
