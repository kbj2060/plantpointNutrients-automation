from abc import abstractmethod
from db import MysqlController
from models.Mqtt import MQTT

ON = 1
OFF = 0
class DeviceManager(MQTT, MysqlController):
    def __init__(self) -> None:
        MQTT.__init__(self)
        MysqlController.__init__(self)
        self.last_automation = None
        self.state = None
        self.status = None
        self.topic = None

    def check_machine_on(self, machine_power):
        return machine_power == 1

    @abstractmethod
    def check_condition(self):
        pass
    
    def control(self):
        if not self.last_automation['active']:
            print('Automation Inactivated')

        elif self.check_condition() and not self.check_machine_on(self.status):
            # self.emit_switch_socket("led", True)
            # self.telegram_post_text(f"자동화에 의해 조명이 켜졌습니다.")
            self.insert_switch(machine_id=self.state['machine_id'], controlledBy='auto', status=ON)
            self.client.publish(self.topic, ON)

        elif not self.check_condition() and self.check_machine_on(self.status):
            # self.emit_switch_socket("led", False)
            # self.telegram_post_text(f"자동화에 의해 조명이 꺼졌습니다.")
            self.insert_switch(machine_id=self.state['machine_id'], controlledBy='auto', status=OFF)
            self.client.publish(self.topic, OFF)

        else:
            print('Do Nothing.')