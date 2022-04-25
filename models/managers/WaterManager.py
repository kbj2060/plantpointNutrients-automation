

import asyncio
from datetime import datetime
import time
from api import post_automation_history, post_report
from models.SensorModels import WaterLevel
from models.managers.ManagerBase import ManagerBase
from halo import Halo
from utils import DB_date

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