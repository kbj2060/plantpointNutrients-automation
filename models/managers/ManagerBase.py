from db import MysqlController


class ManagerBase(MysqlController):
    def __init__(self, switches: dict, automations: dict, sensors: dict) -> None:
        MysqlController.__init__(self)
        self.switches = switches
        self.automations = automations
        self.sensors = sensors

    def _find_switch(self, name):
        return self.switches[name]

    def _find_automation(self, name):
        return self.automations[name]

    def _find_sensor(self, name):
        return self.sensors[name]