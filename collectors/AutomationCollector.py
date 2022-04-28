
from models.AutomationModels import AutomationAC, AutomationBase, AutomationFan, AutomationLed, AutomationRoofFan, SprayTerm, SprayTime, WaterSupply, NutrientSupply
from api import get_last_automation_date, post_automation_history, post_report
from collectors.CollectorBase import CollectorBase
from config import AUTOMATION_TABLES
from datetime import datetime
from utils import DB_date
import asyncio

class AutomationCollector(CollectorBase):
    def _classify_automation_model(self, automations: dict) -> AutomationBase:
        return [
            AutomationAC(**automations['automation_ac']),
            AutomationFan(**automations['automation_fan']),
            AutomationRoofFan(**automations['automation_rooffan']),
            AutomationLed(**automations['automation_led']),
            SprayTerm(**automations['sprayterm']),
            SprayTime(**automations['spraytime']),
            NutrientSupply(**automations['nutrientsupply']),
            WaterSupply(**automations['watersupply'])
        ]
        
    
    def _get_automations(self) -> dict:
        results = {}
        for automation_table in AUTOMATION_TABLES:
            results[automation_table] = self.select_last_automation(automation_table)
        return results

    # @classmethod           
    # def get_last_activated(self, subject, isCompleted=False):
    #     res = asyncio.run(get_last_automation_date(subject, isCompleted))
    #     if res is None or len(res) == 0:
    #         asyncio.run(
    #             post_automation_history(
    #                 subject=subject, 
    #                 createdAt=DB_date(datetime(1990,1,1)), 
    #                 isCompleted=False
    #                 )
    #             )
    #         asyncio.run(post_report(lv=2, problem='자동화 데이터가 존재하지 않아 이전 데이터를 불러올 수 없습니다.'))
    #         return DB_date("1990-01-01T00:00:00")
    #     return res
        
    def get(self):
        automations = self._get_automations()
        return self._classify_automation_model(automations)
