from abc import abstractmethod
from models.managers.Mqtt import MQTT

class DeviceManager(MQTT):
    def __init__(self) -> None:
        MQTT.__init__(self)
        self.off, self.on = 0, 1
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
            self.insert_switch(machine_id=self.state['machine_id'], controlledBy='auto', status=self.on)
            self.client.publish(self.topic, self.on)

        elif not self.check_condition() and self.check_machine_on(self.status):
            # self.emit_switch_socket("led", False)
            # self.telegram_post_text(f"자동화에 의해 조명이 꺼졌습니다.")
            self.insert_switch(machine_id=self.state['machine_id'], controlledBy='auto', status=self.off)
            self.client.publish(self.topic, self.off)

        else:
            print('Do Nothing.')