

import time
from db import MysqlController
from models.managers.DeviceManager import DeviceManager


class LedManager(DeviceManager, MysqlController):
    def __init__(self) -> None:
        DeviceManager.__init__(self)
        MysqlController.__init__(self)
        self.last_automation = self.select_led_automation()
        self.state = self.select_current_state('led')
        self.status = self.state['status']

    def check_led_valid_hour(self):
        current_time = time.strftime('%H:%M:%S', time.localtime(time.time()))
        return self.last_automation['start'] <= current_time < self.last_automation['end']

    def led_control(self):
        topic = self.make_machine_topic('led')
        auto_switch = self.last_automation['active']

        if not auto_switch:
            print('LED Auto Switch Disabled')

        elif self.check_led_valid_hour() and not self.check_machine_on(self.status):
            print("LED ON")
            # self.emit_switch_socket("led", True)
            # self.telegram_post_text(f"자동화에 의해 조명이 켜졌습니다.")
            self.insert_switch(machine_id=self.state['machine_id'], controlledBy='auto', status=self.on)
            self.client.publish(topic, self.on)

        elif not self.check_led_valid_hour() and self.check_machine_on(self.status):
            print("LED OFF")
            # self.emit_switch_socket("led", False)
            # self.telegram_post_text(f"자동화에 의해 조명이 꺼졌습니다.")
            self.insert_switch(machine_id=self.state['machine_id'], controlledBy='auto', status=self.off)
            self.client.publish(topic, self.off)

        else:
            print('LED Do Nothing.')