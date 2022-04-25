import asyncio
from datetime import datetime
from api import post_automation_history, post_report
from config import WATERTANK_HEIGHT, WATERTANK_LIMIT
from models.SensorModels import WaterLevel
from models.SwitchModels import Valve
from halo import Halo
import time
import paho.mqtt.client as mqtt

from utils import DB_date, str2datetime

class MQTT():
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("MQTT connected")
        else:
            print("Bad connection Returned code=", rc)

    def on_disconnect(self, client, userdata, flags, rc=0):
        print("MQTT Disconnected")
        print("-----------------------------------------------------")

    def on_publish(self, client, userdata, mid):
        print("In on_pub callback mid= ", mid)
        
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
        self.upper_waterlevel = self._find_sensor(name='upper_waterlevel')
        self.middle_waterlevel = self._find_sensor(name='middle_waterlevel')
        self.lower_waterlevel = self._find_sensor(name='lower_waterlevel')

    def empty_tank(self):
        spinner = Halo()
        spinner.info('물탱크 비우기 시작합니다.')
        self.valve_out.on()
        timeout = time.time() + 60 * 3
        while not self.lower_waterlevel.get_waterlevel():
            if time.time() > timeout:
                asyncio.run(post_report(lv=3, problem="3분 동안 물이 채워지지 않고 있습니다. 확인바랍니다."))
                raise Exception('3분 동안 물이 채워지지 않고 있습니다. 확인바랍니다.')
            time.sleep(1)
        self.valve_out.off()
        time.sleep(1)
        spinner.info('물탱크 비우기 종료합니다.')

    def water_tank(self, waterlevel: WaterLevel):
        spinner = Halo()
        spinner.info('물탱크 채우기 시작합니다.')
        self.valve_in.on()
        self.waterpump_center.on()
        timeout = time.time() + 60 * 3
        while not waterlevel.get_waterlevel():
            if time.time() > timeout:
                asyncio.run(post_report(lv=3, problem="3분 동안 물이 채워지지 않고 있습니다. 확인바랍니다."))
                raise Exception('3분 동안 물이 채워지지 않고 있습니다. 확인바랍니다.')
            time.sleep(1)
        self.waterpump_center.off()
        self.valve_in.off()
        time.sleep(1)
        spinner.info('물탱크 채우기 종료합니다.')

    def control(self):
        # waterlevel = self.waterlevel.get_waterlevel()
        # print(f"수위는 {waterlevel} cm 입니다.")
        lwl = self.lower_waterlevel.get_waterlevel()
        # if waterlevel < 0 or waterlevel > WATERTANK_HEIGHT:
        #     asyncio.run(post_report(lv=3, problem="수위센서측정에 문제가 생겼습니다."))
        #     raise Exception('수위센서측정에 문제가 생겼습니다.')
        if not lwl:
            asyncio.run(post_automation_history(subject='watersupply', createdAt=DB_date(datetime.now()), isCompleted=False))
            # self.empty_tank()
            self.waterpump_a.supply_nutrient()
            self.water_tank(self.middle_waterlevel)
            self.waterpump_b.supply_nutrient()
            self.water_tank(self.upper_waterlevel)
            asyncio.run(post_automation_history(subject='watersupply', createdAt=DB_date(datetime.now()), isCompleted=True))
        else:
            print("양액 시스템 상태 양호합니다.")
        print("양액 자동화 시스템 종료합니다.")


class SprayManager(ManagerBase):
    def __init__(self, switches: dict, automations: dict, sensors: dict) -> None:
        super().__init__(switches, automations, sensors)
        self.wm = WaterManager(switches, automations, sensors)
        self.waterpump_1 = self._find_switch(name='waterpump_1')
        self.waterpump_2 = self._find_switch(name='waterpump_2')
        self.waterpump_3 = self._find_switch(name='waterpump_3')
        self.waterpump_sprayer = self._find_switch(name='waterpump_sprayer')
        self.spraytime = self._find_automation(name='spraytime')
        self.sprayterm = self._find_automation(name='sprayterm')

    def check_term(self):
        last_term = (datetime.now() - str2datetime(self.automations['spray_activatedAt'])).total_seconds()/60
        if  round(last_term) >= self.sprayterm.period:
            return True

    def spray(self, waterpump, operating_time: int):
        spinner = Halo()
        spinner.info(text=f" 스프레이 작동 중입니다..")
        waterpump.on()
        time.sleep(operating_time)
        waterpump.off()
        time.sleep(1)
        
    def control(self):
        print("스프레이 자동화 시작합니다.")
        if self.check_term():
            asyncio.run(post_automation_history(subject='spray', createdAt= DB_date(datetime.now()), isCompleted=False))
            self.spray(self.waterpump_1, int(self.spraytime.period))
            self.spray(self.waterpump_2, int(self.spraytime.period) + 2)
            self.spray(self.waterpump_3, int(self.spraytime.period) + 4)
            print("스프레이 자동화 종료됩니다.")
            asyncio.run(post_automation_history(subject='spray', createdAt= DB_date(datetime.now()), isCompleted=True))
        else:
            print("스프레이 자동화 작동될 시간이 아닙니다.")


class EnvironmentManager(ManagerBase):
    def __init__(self, sensors: dict) -> None:
        self.sensors = sensors

    def measure_environment(self):
        dht = self._find_sensor('dht22')
        dht.post_humidity_temperature()
