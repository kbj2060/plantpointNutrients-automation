

import asyncio
from datetime import datetime
import time
from models.managers.ManagerBase import ManagerBase
from models.managers.WaterManager import WaterManager
from utils import DB_date, str2datetime
from api import post_automation_history
from halo import Halo

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