from db import MysqlController


class ManagerBase(MysqlController):
    def __init__(self, switches: list, automations: list, sensors: list) -> None:
        MysqlController.__init__(self)
        self.switches = switches
        self.automations = automations
        self.sensors = sensors

    def _find_switch(self, name):
        for _switch in self.switches:
            if _switch.name == name:
                return _switch
        raise Exception('찾는 스위치가 존재하지 않습니다.')

    def _find_automation(self, name):
        for automation in self.automations:
            if automation.name == name:
                return automation
        raise Exception('찾는 자동설정이 존재하지 않습니다.')

    def _find_sensor(self, name):
        for sensor in self.sensors:
            if sensor.name == name:
                return sensor
        raise Exception('찾는 센서가 존재하지 않습니다.')