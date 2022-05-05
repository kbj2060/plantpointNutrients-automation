from config import ON, OFF
import RPi.GPIO as GPIO
from config import NUTRIENT_AMOUNT
from db import MysqlController
from logger import logger
from models.Mqtt import MQTT
from models.WebsocketModel import send_socket
from utils import fDBDate
import json
import time

class SwitchBase(MQTT, MysqlController):
    def __init__(self, id: int, pin:int, name: str, createdAt: str) -> None:
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
        MQTT.__init__(self)
        MysqlController.__init__(self)
        self.id = id
        self.name = name
        self.pin = pin
        self.poweredAt = None
        self.status = None
        self.topic = self.make_machine_topic(self.name)

    @classmethod
    def get_name(cls):
        return cls.__name__.lower()

    def set_switch_info(self, status, poweredAt):
        self.poweredAt = fDBDate(poweredAt)
        self.status = status

    async def on(self):
        GPIO.output(self.pin, GPIO.HIGH)
        await send_socket(json.dumps({ f"{self.name}" : True }))
        self.insert_switch(machine_id=self.id, controlledBy='auto', status=ON)
        self.client.publish(self.topic, ON)
        logger.on(text=f"{self.name} 켜졌습니다.")

    async def off(self):
        GPIO.output(self.pin, GPIO.LOW)
        await send_socket(json.dumps({ f"{self.name}" : False }))
        self.insert_switch(machine_id=self.id, controlledBy='auto', status=OFF)
        self.client.publish(self.topic, OFF)
        logger.off(text=f"{self.name} 꺼졌습니다.")


class Valve(SwitchBase):
    pass

class WaterPump(SwitchBase):
    async def supply_nutrient(self):
        # 20L 당 50ml 양액
        velocity = 40 # ml/sec
        operating_time = NUTRIENT_AMOUNT / velocity
        await self.on()
        time.sleep(operating_time)
        await self.off()
        time.sleep(0.5)

class WaterSpray(SwitchBase):
    pass


class LED(SwitchBase):
    pass

class Fan(SwitchBase):
    pass

class RoofFan(SwitchBase):
    pass

class AirConditioner(SwitchBase):
    pass
