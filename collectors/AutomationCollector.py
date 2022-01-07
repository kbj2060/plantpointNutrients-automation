
import asyncio
from api import get_last_automation_date, get_last_automations
from collectors.CollectorBase import CollectorBase
from models.AutomationModels import AutomationBase, SprayTerm, SprayTime, WaterSupply, NutrientSupply

AUTOMATION_SUBJECTS = ['nutrientsupply', 'spraytime', 'sprayterm', 'watersupply']
AUTOMATION_MODELS = [SprayTerm, SprayTime, WaterSupply, NutrientSupply]

class AutomationCollector(CollectorBase):
    def _classify_automation_model(self, automations: list) -> AutomationBase:
        results = {}
        for automation in automations:
            found_automation_model = next(a_model for a_model in AUTOMATION_MODELS if a_model.get_name() == automation['name'])
            results[automation['name']] = found_automation_model(**automation)
        return results

    def _get_automations(self) -> dict:
        try:
            return [{**asyncio.run(get_last_automations(model.get_name())), 'name': model.get_name()} for model in AUTOMATION_MODELS]
        except:
            self.error_handling('데이터 쿼리')
            
    def get_last_activated(self):
        res = asyncio.run(get_last_automation_date())
        return res.start
        
    def get(self):
        automations = self._get_automations()
        automation_models = self._classify_automation_model(automations)
        if not (len(automations) == len(automation_models) == len(AUTOMATION_SUBJECTS)):
            self.error_handling('Automation 데이터 검증')
        automation_models['activatedAt'] = self.get_last_activated()
        return automation_models