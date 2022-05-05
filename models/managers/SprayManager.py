from datetime import datetime
from api import post_automation_history, post_report
from logger import logger
from models.AutomationModels import AutomationBase, SprayTerm, SprayTime
from models.SensorModels import SensorBase
from models.SwitchModels import SwitchBase, WaterSpray
from models.managers.ManagerBase import ManagerBase
from models.managers.WaterManager import WaterManager
from halo import Halo
from typing import List
import asyncio
import time
from utils import DB_date


class SprayManager(ManagerBase):
    def __init__(self, switches: List[SwitchBase], automations: List[AutomationBase], sensors: List[SensorBase]) -> None:
        super().__init__(switches, automations, sensors)
        self.wm = WaterManager(switches, automations, sensors)

        self.waterspray_1: WaterSpray = self._find_switch(name='waterspray_1')
        self.waterspray_2: WaterSpray = self._find_switch(name='waterspray_2')
        self.waterspray_3: WaterSpray = self._find_switch(name='waterspray_3')

        self.spraytime: SprayTime = self._find_automation(name='spraytime')
        self.sprayterm: SprayTerm = self._find_automation(name='sprayterm')

    def get_last_activated(self):
        res = self.select_last_automation_activated('spray')
        if res is None or len(res) == 0:
            asyncio.run(
                post_automation_history(
                    subject='spray', 
                    createdAt=DB_date(datetime(1990,1,1)), 
                    isCompleted=False
                    )
                )
            asyncio.run(post_report(lv=2, problem='자동화 데이터가 존재하지 않아 이전 데이터를 불러올 수 없습니다.'))
            return DB_date("1990-01-01T00:00:00")
        return res
        
    def check_term(self):
        last_activatedAt = self.get_last_activated()
        last_term = (datetime.now() - last_activatedAt['createdAt']).total_seconds()/60
        return round(last_term) >= self.sprayterm.period

    async def spray(self, waterspray: WaterSpray, operating_time: int):
        logger.info(text=f" 스프레이 작동 중입니다..")
        await waterspray.on()
        time.sleep(operating_time)
        await waterspray.off()
        time.sleep(1)
        
    def control(self):
        logger.info("스프레이 자동화 시작합니다.")
        if self.check_term():
            self.insert_automation_history(subject='spray', isCompleted=False)
            asyncio.run(self.spray(self.waterspray_1, int(self.spraytime.period)))
            asyncio.run(self.spray(self.waterspray_2, int(self.spraytime.period) + 1))
            asyncio.run(self.spray(self.waterspray_3, int(self.spraytime.period) + 2))
            self.insert_automation_history(subject='spray', isCompleted=True)
            logger.info("스프레이 자동화 종료됩니다.")
        else:
            logger.error("스프레이 자동화 작동될 시간이 아닙니다.")