
import asyncio
from api import get_last_automation_date, get_last_automations, post_automation_history, post_report
from collectors.CollectorBase import CollectorBase
from config import AUTOMATION_TABLES
from models.AutomationModels import AutomationAC, AutomationBase, AutomationFan, AutomationLed, AutomationRoofFan, SprayTerm, SprayTime, WaterSupply, NutrientSupply
from datetime import datetime
import pymysql
from utils import DB_date

class AutomationCollector(CollectorBase):
    def _classify_automation_model(self, automations: dict) -> AutomationBase:
        # results = {}
        # for automation in automations:
        #     found_automation_model = next(a_model for a_model in AUTOMATION_MODELS if a_model.get_name() == automation['name'])
        #     results[automation['name']] = found_automation_model(**automation)
        # return results
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
        # try:
        #     return [{**asyncio.run(get_last_automations(model.get_name())), 'name': model.get_name()} for model in AUTOMATION_MODELS]
        # except:
        #     self.error_handling('데이터 쿼리')
    
    @classmethod           
    def get_last_activated(self, subject, isCompleted=False):
        res = asyncio.run(get_last_automation_date(subject, isCompleted))
        if res is None or len(res) == 0:
            asyncio.run(
                post_automation_history(
                    subject=subject, 
                    createdAt=DB_date(datetime(1990,1,1)), 
                    isCompleted=False
                    )
                )
            asyncio.run(post_report(lv=2, problem='자동화 데이터가 존재하지 않아 이전 데이터를 불러올 수 없습니다.'))
            return DB_date("1990-01-01T00:00:00")
        return res
        
    def get(self):
        automations = self._get_automations()
        return self._classify_automation_model(automations)
        # automations = self._get_automations()
        # automation_models = self._classify_automation_model(automations)
        # if not (len(automations) == len(automation_models) == len(AUTOMATION_SUBJECTS)):
        #     self.error_handling('Automation 데이터 검증')
        # automation_models['spray_activatedAt'] = self.get_last_activated('spray')['createdAt']
        # automation_models['watersupply_activatedAt'] = self.get_last_activated('watersupply')['createdAt']
        # return automation_models
