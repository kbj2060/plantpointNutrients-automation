import asyncio
from halo import Halo
import RPi.GPIO as GPIO
import Adafruit_DHT as dht
from api import post_humidity, post_temperature, post_report
import spidev
from config import CURRENT_LIMIT, SPICLK, SPICS, SPIMISO, SPIMOSI
import time
import itertools
import Adafruit_GPIO.SPI as SPI
from utils import detect_outlier

class MCP3208:
    def __init__(self, channel):        
        GPIO.setup(SPIMOSI, GPIO.OUT)
        GPIO.setup(SPIMISO, GPIO.IN)
        GPIO.setup(SPICLK, GPIO.OUT)
        GPIO.setup(SPICS, GPIO.OUT)
        self.channel = channel

    def read(self):
        if ((self.channel > 7) or (self.channel < 0)):
                return -1
        GPIO.output(SPICS, True)      # CS핀을 high로 만든다.
        GPIO.output(SPICLK, False)  # clock핀을 low로 만든다. 시작한다.
        GPIO.output(SPICS, False)     # CS핀을 low로 만든다.
        commandout = self.channel
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(SPIMOSI, True)
                else:
                        GPIO.output(SPIMOSI, False)
                commandout <<= 1
                GPIO.output(SPICLK, True)
                GPIO.output(SPICLK, False)
        adcout = 0
        for i in range(14):
                GPIO.output(SPICLK, True)
                GPIO.output(SPICLK, False)
                adcout >>= 1
                if (GPIO.input(SPIMISO)):
                        adcout |= 0x1
        GPIO.output(SPICS, True)
        adcout <<= 1       # first bit is 'null' so drop it
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
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def measure_waterlevel(self):
        return True if GPIO.input(self.pin) else False

    def get_waterlevel(self):
        results = []
        for _ in itertools.repeat(None, 5):
            results.append(self.measure_waterlevel())
        if not self.all_equal(results):
            post_report(lv=2, problem="waterlevel values are not equal")
            print("수위 센서의 값이 일정하지 않습니다. 확인 바랍니다.")
            return True if results.count(True) > results.count(False) else False
        return results[0]

    def all_equal(self, lst):
        return lst.count(lst[0]) == len(lst)

class DHT22(SensorModel):
    def __init__(self, id: int, name: str, pin: int, createdAt: str) -> None:
        super().__init__(id, name, pin, createdAt)

    def get_values(self):
        humidity, temperature = dht.read_retry(dht.DHT22, self.pin)
        return humidity, temperature

    def post_humidity_temperature(self):
        humidity, temperature = self.get_values()
        print(f"온도 : {temperature} / 습도 : {humidity}")
        if humidity is not None and temperature is not None:
            asyncio.run(post_temperature(temperature))
            asyncio.run(post_humidity(humidity))
