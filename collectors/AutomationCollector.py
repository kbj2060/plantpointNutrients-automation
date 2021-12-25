
import asyncio
from api import get_last_automations, post_report
from config import AUTOMATION_MODELS, AUTOMATION_SUBJECTS
from models.AutomationModels import AutomationBase


def error_handling(point) -> None:
    asyncio.run(post_report(lv=3, problem=f'[Automation] {point}에 문제가 생겼습니다.'))   
    raise Exception(f'[Automation] {point}에 문제가 생겼습니다.')

class AutomationCollector:
    def _classify_automation_model(self, automation: dict) -> AutomationBase:
        for model in AUTOMATION_MODELS:
            if model.get_name() == automation['name']: return model(**automation)

    def _get_automations(self) -> dict:
        try:
            return [{**asyncio.run(get_last_automations(subject)), 'name': subject} for subject in AUTOMATION_SUBJECTS]
        except:
            error_handling('데이터 쿼리')

    def get(self):
        automations = self._get_automations()
        automation_models = [ self._classify_automation_model(automation) for automation in automations ]
        if not (len(automations) == len(automation_models) == len(AUTOMATION_SUBJECTS)):
            error_handling('Automation 데이터 검증')
        return automation_models