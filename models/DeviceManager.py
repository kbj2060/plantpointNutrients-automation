
import time
import paho.mqtt.client as mqtt
from config import CLIENT_ID, MQTT_HOST, MQTT_PORT, SECTION
from db import MysqlController
from datetime import datetime


class MQTT():
    def __init__(self) -> None:
        self.client = mqtt.Client(client_id=CLIENT_ID)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        self.client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("MQTT connected")
        else:
            print("Bad connection Returned code=", rc)

    def on_disconnect(self, client, userdata, flags, rc=0):
        print("MQTT Disconnected")
        print("-----------------------------------------------------")

    def on_publish(self, client, userdata, mid):
        pass
    
    def make_machine_topic(self, machine):
        return f"{SECTION}/{machine}"

class DeviceManager(MQTT):
    def __init__(self) -> None:
        MQTT.__init__(self)
        self.off, self.on = 0, 1

    def check_machine_on(self, machine_power):
        return machine_power == 1

class LedManager(DeviceManager, MysqlController):
    def __init__(self) -> None:
        DeviceManager.__init__(self)
        MysqlController.__init__(self)
        self.last_automation = self.select_led_automation()
        self.led_state = self.select_current_state('led')
        self.led_status = self.led_state['status']

    def check_led_valid_hour(self):
        current_time = time.strftime('%H:%M:%S', time.localtime(time.time()))
        return self.last_automation['start'] <= current_time < self.last_automation['end']

    def led_control(self):
        topic = self.make_machine_topic('led')
        auto_switch = self.last_automation['active']

        if not auto_switch:
            print('LED Auto Switch Disabled')

        elif self.check_led_valid_hour() and not self.check_machine_on(self.led_status):
            print("LED ON")
            # self.emit_switch_socket("led", True)
            # self.telegram_post_text(f"자동화에 의해 조명이 켜졌습니다.")
            self.insert_switch(machine_id=self.led_state['machine_id'], controlledBy='auto', status=self.on)
            self.client.publish(topic, self.on)

        elif not self.check_led_valid_hour() and self.check_machine_on(self.led_status):
            print("LED OFF")
            # self.emit_switch_socket("led", False)
            # self.telegram_post_text(f"자동화에 의해 조명이 꺼졌습니다.")
            self.insert_switch(machine_id=self.led_state['machine_id'], controlledBy='auto', status=self.off)
            self.client.publish(topic, self.off)

        else:
            print('LED Do Nothing.')
