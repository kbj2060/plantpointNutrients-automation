from collectors.CollectorBase import CollectorBase
from models.SwitchModels import AirConditioner, Fan, RoofFan, SwitchBase, Valve, WaterPump, LED, WaterSpray

class SwitchCollector(CollectorBase):
    def _classify_machine_model(self, machines: dict):
        results = []
        for machine in machines:
            name = machine['name']
            if 'valve' in name:
                tmp = Valve(**machine)
            elif 'waterpump' in name:
                tmp = WaterPump(**machine)
            elif 'waterspray' in name:
                tmp = WaterSpray(**machine)
            elif 'led' in name:
                tmp = LED(**machine)
            elif 'fan' == name:
                tmp = Fan(**machine)
            elif 'rooffan' == name:
                tmp = RoofFan(**machine)
            elif 'airconditioner' == name:
                tmp = AirConditioner(**machine)
            else:
                raise Exception('해당되는 디바이스가 존재하지 않습니다.')
            results.append(tmp)
        return results

    def _get_machines(self):
        return self.select_machines()

    def get(self):
        machines = self._get_machines()
        return self._classify_machine_model(machines)
