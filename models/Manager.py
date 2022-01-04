from datetime import datetime
from api import post_report
from config import WATERTANK_HEIGHT
from models.SensorModels import DHT22
from models.SwitchModels import Valve
from halo import Halo
import time


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

    def empty_tank(self):
        spinner = Halo()
        spinner.info('물탱크 비우기 시작합니다.')
        self.valve_out.on()
        while self.waterlevel.get_waterlevel() <= 1: # 1cm
            time.sleep(1)
        self.valve_out.off()
        time.sleep(1)
        spinner.info('물탱크 비우기 종료합니다.')

    def water_tank(self, height):
        spinner = Halo()
        spinner.info('물탱크 채우기 시작합니다.')
        self.valve_in.on()
        self.waterpump_center.on()
        while self.waterlevel.get_waterlevel() >= height:
            time.sleep(1)
        self.waterpump_center.off()
        self.valve_in.off()
        time.sleep(1)
        spinner.info('물탱크 채우기 종료합니다.')

    def control(self):
        print("양액 자동화 시스템 시작합니다.")
        waterlevel = self.waterlevel.get_waterlevel()
        print(f"수위는 {waterlevel} cm 입니다.")
        if waterlevel < 0 or waterlevel > WATERTANK_HEIGHT:
            post_report(lv=3, problem="수위센서측정에 문제가 생겼습니다.")
            raise Exception('수위센서측정에 문제가 생겼습니다.')
        elif waterlevel <= WATERTANK_HEIGHT * 0.05:
            self.empty_tank()
            self.waterpump_a.supply_nutrient()
            self.water_tank(WATERTANK_HEIGHT//2)
            self.waterpump_b.supply_nutrient()
            self.water_tank(WATERTANK_HEIGHT * 0.95)
        else:
            print("양액 시스템 상태 양호합니다.")
        print("양액 자동화 시스템 종료합니다.")


class SprayManager(ManagerBase):
    def __init__(self, switches: dict, automations: dict, sensors: dict) -> None:
        super().__init__(switches, automations, sensors)
        self.valve_1 = self._find_switch(name='valve_1')
        self.valve_2 = self._find_switch(name='valve_2')
        self.valve_3 = self._find_switch(name='valve_3')
        self.waterpump_sprayer = self._find_switch(name='waterpump_sprayer')
        self.spraytime = self._find_automation(name='spraytime')
        self.sprayterm = self._find_automation(name='sprayterm')
    
    def spray(self, valve: Valve, operating_time: int):
        floor = valve.name.split('_')[1]
        spinner = Halo()
        spinner.info(text=f"{floor}층 스프레이 작동 중입니다..")
        valve.on()
        time.sleep(0.2)
        self.waterpump_sprayer.on()
        time.sleep(operating_time)
        self.waterpump_sprayer.off()
        time.sleep(0.2)
        valve.off()
        time.sleep(0.2)

    def control(self):
        print("스프레이 자동화 시작합니다.")
        last_term = (datetime.now() - self.waterpump_sprayer.poweredAt).total_seconds()/60
        if last_term >= self.sprayterm.period: # minutes
            self.spray(self.valve_1, int(self.spraytime.period))
            self.spray(self.valve_2, int(self.spraytime.period) + 2)
            self.spray(self.valve_3, int(self.spraytime.period) + 4)
            print("스프레이 자동화 종료됩니다.")
        else:
            print("스프레이 자동화 작동될 시간이 아닙니다.")
        
class EnvironmentManager(ManagerBase):
    def __init__(self, sensors: dict) -> None:
        self.sensors = sensors

    def measure_environment(self):
        dht = self._find_sensor('dht22')
        dht.post_humidity_temperature()
