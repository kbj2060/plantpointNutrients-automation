from datetime import datetime
from api import post_report
from config import WATERTANK_HEIGHT
from models.SensorModels import DHT22
from models.SwitchModels import Valve
from halo import Halo
import time

from utils import sleep_with_text


class ManagerBase:
    def __init__(self, switches: dict, automations: dict, sensors: dict) -> None:
        self.switches = switches
        self.automations = automations
        self.sensors = sensors

    def _find_switch(self, name):
        return self.switches[name]

    def _find_automation(self, name):
        return self.automations[name]

    def _find_sensor(self, name):
        return self.sensors[name]


class WaterManager(ManagerBase):
    def __init__(self, switches: dict, automations: dict, sensors: dict) -> None:
        super().__init__(switches, automations, sensors)
        self.waterpump_center = self._find_switch(name='waterpump_center')
        self.valve_in = self._find_switch(name='valve_in')
        self.valve_out = self._find_switch(name='valve_out')
        self.waterpump_a = self._find_switch(name='waterpump_a')
        self.waterpump_b = self._find_switch(name='waterpump_b')
        self.watersupply = self._find_automation(name='watersupply')
        self.nutrientsupply = self._find_automation(name='nutrientsupply')
        self.waterlevel = self._find_sensor(name='waterlevel')
        self.vi_current = self._find_sensor(name='vi_current')
        self.vo_current = self._find_sensor(name='vo_current')
        self.wpa_current = self._find_sensor(name='wpa_current')
        self.wpb_current = self._find_sensor(name='wpb_current')

    def empty_tank(self):
        self.valve_out.on()
        while self.waterlevel.get_waterlevel() <= 1: # 1cm
            time.sleep(1)
        self.valve_out.off()
        time.sleep(1)
    
    def water_tank(self, height):
        self.valve_in.on()
        self.waterpump_center.on()
        while self.waterlevel.get_waterlevel() >= height:
            time.sleep(1)
        self.waterpump_center.off()
        self.valve_in.off()
        time.sleep(1)

    def control(self):
        waterlevel = self.waterlevel.get_waterlevel()
        if waterlevel < 0 or waterlevel > WATERTANK_HEIGHT:
            post_report(lv=3, problem="수위센서측정에 문제가 생겼습니다.")
            raise Exception('수위센서측정에 문제가 생겼습니다.')
        elif waterlevel <= WATERTANK_HEIGHT * 0.05:
            self.empty_tank()
            self.waterpump_a.supply_nutrient()
            self.water_tank(WATERTANK_HEIGHT//2)
            self.waterpump_b.supply_nutrient()
            self.water_tank(WATERTANK_HEIGHT * 0.95)


class SprayManager(ManagerBase):
    def __init__(self, switches: dict, automations: dict, sensors: dict) -> None:
        super().__init__(switches, automations, sensors)
        self.valve_1 = self._find_switch(name='valve_1')
        self.valve_2 = self._find_switch(name='valve_2')
        self.valve_3 = self._find_switch(name='valve_3')
        self.waterpump_sprayer = self._find_switch(name='waterpump_sprayer')
        self.spraytime = self._find_automation(name='spraytime')
        self.sprayterm = self._find_automation(name='sprayterm')
        self.v1_current = self._find_sensor(name='v1_current')
        self.v2_current = self._find_sensor(name='v2_current')
        self.v3_current = self._find_sensor(name='v3_current')
        self.wps_current = self._find_sensor(name='wps_current')
    
    def spray(self, valve: Valve, operating_time: int):
        valve.on()
        time.sleep(0.1)
        self.waterpump_sprayer.on()
        sleep_with_text(waiting_time=operating_time, text=f"Spraying..")
        self.waterpump_sprayer.off()
        time.sleep(0.1)
        valve.off()
        time.sleep(1)

    def control(self):
        last_term = (datetime.now() - self.waterpump_sprayer.poweredAt).total_seconds()/60
        if last_term >= self.sprayterm.period: # minutes
            spinner = Halo(text="WaterSpray Automation Started!", spinner='dots')
            spinner.start()
            self.spray(self.valve_1, int(self.spraytime.period))
            self.spray(self.valve_2, int(self.spraytime.period) + 2)
            self.spray(self.valve_3, int(self.spraytime.period) + 4)
            spinner.stop()
        else:
            print("No time to spray!")
            
class EnvironmentManager(ManagerBase):
    def __init__(self, sensors: dict) -> None:
        self.sensors = sensors

    def measure_environment(self):
        dht = self._find_sensor('dht22')
        dht.post_humidity_temperature()
