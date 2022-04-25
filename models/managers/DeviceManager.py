from models.managers.Mqtt import MQTT

class DeviceManager(MQTT):
    def __init__(self) -> None:
        MQTT.__init__(self)
        self.off, self.on = 0, 1

    def check_machine_on(self, machine_power):
        return machine_power == 1
