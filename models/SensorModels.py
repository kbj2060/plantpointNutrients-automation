import asyncio
from halo import Halo
import RPi.GPIO as GPIO
import Adafruit_DHT as dht
from api import post_humidity, post_temperature
import spidev
from config import CLOCKPIN, CSPIN, CURRENT_LIMIT, MISOPIN, MOSIPIN, WATERTANK_HEIGHT
import time
import itertools
import Adafruit_GPIO.SPI as SPI
from utils import detect_outlier

class MCP3208:
    def __init__(self, channel):        
        SPICLK = 11
        SPIMISO = 9
        SPIMOSI = 10
        SPICS = 8
        GPIO.setup(SPIMOSI, GPIO.OUT)
        GPIO.setup(SPIMISO, GPIO.IN)
        GPIO.setup(SPICLK, GPIO.OUT)
        GPIO.setup(SPICS, GPIO.OUT)
        self.channel = channel

    def read(self):
        if ((self.channel > 7) or (self.channel < 0)):
                return -1
        GPIO.output(self.SPICS, True)      # CS핀을 high로 만든다.
        GPIO.output(self.SPICLK, False)  # clock핀을 low로 만든다. 시작한다.
        GPIO.output(self.SPICS, False)     # CS핀을 low로 만든다.
        commandout = self.channel
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(self.SPIMOSI, True)
                else:
                        GPIO.output(self.SPIMOSI, False)
                commandout <<= 1
                GPIO.output(self.SPICLK, True)
                GPIO.output(self.SPICLK, False)
        adcout = 0
        for i in range(14):
                GPIO.output(self.SPICLK, True)
                GPIO.output(self.SPICLK, False)
                adcout <<= 1
                if (GPIO.input(self.SPIMISO)):
                        adcout |= 0x1
        GPIO.output(self.SPICS, True)
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout      # adcout는 0부터 4095까지 값을 갖는다.

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
        self.adc = MCP3208(pin)

    @Halo(text='Measuring Current..', spinner='dots')
    def measure_current(self):
        return self.adc.read()

    def get_current(self, val_num=3):
        results = []
        for _ in itertools.repeat(None, val_num):
            results.append(self.measure_current())
        outliers = detect_outlier(results)
        if outliers:
            results = [item for item in results if item not in outliers]
        return sum(results)/len(results)

class WaterLevel(SensorModel):
    def __init__(self, id: int, name: str, pin: int, createdAt: str) -> None:
        super().__init__(id, name, pin, createdAt)
        self.adc = MCP3208(pin)
        # GPIO.setup(self.pin, GPIO.OUT)
        # GPIO.setup(self.pin+1, GPIO.IN)

    def measure_waterlevel(self):
        return self.adc.read()
        # GPIO.output(self.pin, GPIO.LOW)         
        # time.sleep(0.5)

        # GPIO.output(self.pin, GPIO.HIGH)
        # time.sleep(0.00001)
        # GPIO.output(self.pin, GPIO.LOW)

        # while GPIO.input(self.pin+1) == 0:
        #     start = time.time()

        # while GPIO.input(self.pin+1) == 1:
        #     stop = time.time()

        # time_interval = stop - start      
        # distance = time_interval * 17000
        # distance = round(distance, 2)
        # return round(WATERTANK_HEIGHT - distance, 1)

    def get_waterlevel(self):
        results = []
        for _ in itertools.repeat(None, 10):
            results.append(self.measure_waterlevel())
        outliers = detect_outlier(results)
        if outliers:
            results = [item for item in results if item not in outliers]
        return 1 if sum(results)/len(results) >= CURRENT_LIMIT else 0

class DHT22(SensorModel):
    def __init__(self, id: int, name: str, pin: int, createdAt: str) -> None:
        super().__init__(id, name, pin, createdAt)

    def post_humidity_temperature(self):
        humidity, temperature = dht.read_retry(dht.DHT22, self.pin)
        print(f"온도 : {temperature} / 습도 : {humidity}")
        if humidity is not None and temperature is not None:
            asyncio.run(post_temperature(temperature))
            asyncio.run(post_humidity(humidity))
