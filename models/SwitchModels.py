import asyncio
import RPi.GPIO as GPIO
from abc import ABCMeta
from api import post_switch
from config import NUTRIENT_AMOUNT, WATERTANK_HEIGHT
from utils import fDBDate
import time

class SwitchBase(metaclass=ABCMeta):
    def __init__(self, id: int, pin:int, name: str, createdAt: str) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
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
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(0.5)
        asyncio.run(post_switch(name=self.name, machine_id=self.id, status=1, controlledBy='auto'))

    def off(self):
        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(0.5)
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
    def supply_water(self):
        self.on()
        while self.waterlevel.get_waterlevel() >= WATERTANK_HEIGHT * 0.9:
            time.sleep(0.1)
        self.off()
        time.sleep(1)

    def supply_nutrient(self):
        # 20L 당 50ml
        velocity = 40 # ml/sec
        operating_time = NUTRIENT_AMOUNT / velocity
        self.on()
        time.sleep(operating_time)
        self.off()
        time.sleep(1)


class LED(SwitchBase):
    pass
