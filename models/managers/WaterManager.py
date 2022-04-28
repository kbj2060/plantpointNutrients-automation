from api import post_report
from logger import logger
from models.AutomationModels import NutrientSupply, WaterSupply
from models.SensorModels import WaterLevel
from models.SwitchModels import Valve, WaterPump
from models.WebsocketModel import send_ping
from models.managers.ManagerBase import ManagerBase
from config import WATER_TANK_MAX_MINUTES
import asyncio
import time

class WaterException(Exception):
    pass

class WaterManager(ManagerBase):
    def __init__(self, switches: list, automations: list, sensors: list) -> None:
        super().__init__(switches, automations, sensors)
        self.valve_in: Valve = self._find_switch(name='valve_in')
        self.valve_out: Valve = self._find_switch(name='valve_out')
        self.waterpump_a: WaterPump = self._find_switch(name='waterpump_a')
        self.waterpump_b: WaterPump = self._find_switch(name='waterpump_b')
        self.waterpump_center: WaterPump = self._find_switch(name='waterpump_center')

        self.watersupply: WaterSupply = self._find_automation(name='watersupply')
        self.nutrientsupply: NutrientSupply = self._find_automation(name='nutrientsupply')

        self.top_waterlevel: WaterLevel = self._find_sensor(name='top_waterlevel')
        self.middle_waterlevel: WaterLevel = self._find_sensor(name='middle_waterlevel')
        self.bottom_waterlevel: WaterLevel = self._find_sensor(name='bottom_waterlevel')

    def reach_waterlevel(self, value: bool):
        return True if value is True else False

    async def empty_tank(self):
        logger.info('물탱크 비우기 시작합니다.')
        await self.valve_out.on()
        timeout = time.time() + 60 * WATER_TANK_MAX_MINUTES
        while self.reach_waterlevel(self.bottom_waterlevel.get_waterlevel()):
            if time.time() > timeout:
                asyncio.run(post_report(lv=3, problem=f"{WATER_TANK_MAX_MINUTES}분 동안 물이 비워지지 않고 있습니다. 확인바랍니다."))
                raise WaterException(f'{WATER_TANK_MAX_MINUTES}분 동안 물이 비워지지 않고 있습니다. 확인바랍니다.')
            time.sleep(10)
            await send_ping()
        await self.valve_out.off()
        time.sleep(1)
        logger.info('물탱크 비우기 종료합니다.')

    async def water_tank(self, target_waterlevel: WaterLevel):
        logger.info('물탱크 채우기 시작합니다.')
        await self.valve_in.on()
        await self.waterpump_center.on()
        timeout = time.time() + 60 * WATER_TANK_MAX_MINUTES
        while not self.reach_waterlevel(target_waterlevel.get_waterlevel()):
            if time.time() > timeout:
                await post_report(lv=3, problem=f"{WATER_TANK_MAX_MINUTES}분 동안 물이 채워지지 않고 있습니다. 확인바랍니다.")
                await self.waterpump_center.off()
                await self.valve_in.off()
                raise WaterException(f'{WATER_TANK_MAX_MINUTES}분 동안 물이 채워지지 않고 있습니다. 확인바랍니다.')
            time.sleep(10)
            await send_ping()
        await self.waterpump_center.off()
        await self.valve_in.off()
        time.sleep(1)
        logger.info('물탱크 채우기 종료합니다.')

    def control(self):
        bwl = self.bottom_waterlevel.get_waterlevel()
        if not self.reach_waterlevel(bwl):
            self.insert_automation_history(subject='watersupply', isCompleted=False)
            asyncio.run(self.water_tank(self.middle_waterlevel))
            asyncio.run(self.waterpump_a.supply_nutrient())
            asyncio.run(self.water_tank(self.top_waterlevel))
            asyncio.run(self.waterpump_b.supply_nutrient())
            self.insert_automation_history(subject='watersupply', isCompleted=True)
        else:
            logger.info("양액 시스템 상태 양호합니다.")
        logger.info("양액 자동화 시스템 종료합니다.")