import asyncio
# import RPi.GPIO as GPIO
from abc import ABCMeta
from api import post_report, post_switch
from config import NUTRIENT_AMOUNT
from utils import fDBDate, turn_off_log, turn_on_log
import time

class SwitchBase(metaclass=ABCMeta):
    def __init__(self, id: int, pin:int, name: str, createdAt: str) -> None:
        # GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
        self.id = id
        self.name = name
        self.pin = pin
        self.poweredAt = None
        self.status = None
    
    @classmethod
    def get_name(cls):
        return cls.__name__.lower()

    def set_switch_info(self, status, poweredAt):
        self.poweredAt = fDBDate(poweredAt)
        self.status = status

    def on(self):
        # GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(0.5)
        turn_on_log(text=f"{self.name} 켜졌습니다.")
        asyncio.run(post_switch(name=self.name, machine_id=self.id, status=1, controlledBy='auto'))

    def off(self):
        # GPIO.output(self.pin, GPIO.LOW)
        time.sleep(0.5)
        turn_off_log(text=f"{self.name} 꺼졌습니다.")
        asyncio.run(post_switch(name=self.name, machine_id=self.id, status=0, controlledBy='auto'))

    def pprint(self):
        print({
            'id': self.id,
            'name': self.name,
            'pin': self.pin,
            'poweredAt': self.poweredAt,
            'status': self.status
        })


class Valve(SwitchBase):
    pass

class WaterPump(SwitchBase):
    def supply_nutrient(self):
        # 20L 당 50ml 양액
        velocity = 40 # ml/sec
        operating_time = NUTRIENT_AMOUNT / velocity
        self.on()
        time.sleep(operating_time)
        self.off()
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
