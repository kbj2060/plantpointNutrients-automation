import asyncio
from halo import Halo
import RPi.GPIO as GPIO
import Adafruit_DHT as dht
from api import post_humidity, post_temperature
import spidev
from config import CLOCKPIN, CSPIN, MISOPIN, MOSIPIN, WATERTANK_HEIGHT
import time


class SensorModel:
    def __init__(self, id: int, name: str, pin: int, createdAt: str) -> None:
        self.id = id
        self.name = name
        self.pin = pin

    @classmethod
    def get_name(cls):
        return cls.__name__.lower()

class Current(SensorModel):
    def __init__(self, id: int, name: str, pin: int, createdAt: str) -> None:
        super().__init__(id, name, pin, createdAt)
        GPIO.setup(MOSIPIN, GPIO.OUT)
        GPIO.setup(MISOPIN, GPIO.IN)
        GPIO.setup(CLOCKPIN, GPIO.OUT)
        GPIO.setup(CSPIN, GPIO.OUT)
        self.channel = pin
        self.cspin = CSPIN
        self.clockpin = CLOCKPIN
        self.mosipin = MOSIPIN
        self.misopin = MISOPIN

    @Halo(text='Measuring Current..', spinner='dots')
    def get_current(self):
        if ((self.channel > 7) or (self.channel < 0)):
            return
        GPIO.output(self.cspin, True)      # CS핀을 high로 만든다.
        GPIO.output(self.clockpin, False)  # clock핀을 low로 만든다. 시작한다.
        GPIO.output(self.cspin, False)     # CS핀을 low로 만든다.
        commandout = self.channel
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
            if (commandout & 0x80):
                GPIO.output(self.mosipin, True)
            else:
                GPIO.output(self.mosipin, False)
            commandout <<= 1
            GPIO.output(self.clockpin, True)
            GPIO.output(self.clockpin, False)
        adcout = 0
        for i in range(14):
            GPIO.output(self.clockpin, True)
            GPIO.output(self.clockpin, False)
            adcout <<= 1
            if (GPIO.input(self.misopin)):
                adcout |= 0x1
        GPIO.output(self.cspin, True)
        adcout <<= 1       # first bit is 'null' so drop it
        return adcout


class WaterLevel(SensorModel):
    def __init__(self, id: int, name: str, pin: int, createdAt: str) -> None:
        super().__init__(id, name, pin, createdAt)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.setup(self.pin+1, GPIO.IN)

    @Halo(text='Measuring WaterLevel..', spinner='dots')
    def get_waterlevel(self):
        # try:
        GPIO.output(self.pin, GPIO.LOW)         
        time.sleep(0.5)

        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.pin, GPIO.LOW)

        while GPIO.input(self.pin+1) == 0:
            start = time.time()

        while GPIO.input(self.pin+1) == 1:
            stop = time.time()

        time_interval = stop - start      
        distance = time_interval * 17000
        distance = round(distance, 2)
        print(f"WaterLevel: {distance}")
        return WATERTANK_HEIGHT - distance
        # except:
        #     

class DHT22(SensorModel):
    def __init__(self, id: int, name: str, pin: int, createdAt: str) -> None:
        super().__init__(id, name, pin, createdAt)

    @Halo(text='Measuring Temperature and Humidity..', spinner='dots')
    def post_humidity_temperature(self):
        humidity, temperature = dht.read_retry(dht.DHT22, self.pin)
        print(f"Temperature : {temperature} / Humidity : {humidity}")
        if humidity is not None and temperature is not None:
            asyncio.run(post_temperature(temperature))
            asyncio.run(post_humidity(humidity))
