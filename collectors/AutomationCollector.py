
import asyncio
from api import get_last_automations, post_report
from collectors.CollectorBase import CollectorBase
from config import AUTOMATION_MODELS, AUTOMATION_SUBJECTS
from models.AutomationModels import AutomationBase




class AutomationCollector(CollectorBase):
    def _classify_automation_model(self, automations: list) -> AutomationBase:
        results = {}
        for automation in automations:
            found_automation_model = next(a_model for a_model in AUTOMATION_MODELS if a_model.get_name() == automation['name'])
            results[automation['name']] = found_automation_model(**automation)
        return results

    def _get_automations(self) -> dict:
        try:
            return [{**asyncio.run(get_last_automations(subject)), 'name': subject} for subject in AUTOMATION_SUBJECTS]
        except:
            self.error_handling('데이터 쿼리')

    def get(self):
        automations = self._get_automations()
        automation_models = self._classify_automation_model(automations)
        if not (len(automations) == len(automation_models) == len(AUTOMATION_SUBJECTS)):
            self.error_handling('Automation 데이터 검증')
        return automation_models