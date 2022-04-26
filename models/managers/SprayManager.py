from datetime import datetime
import time
from models.AutomationModels import SprayTerm, SprayTime
from models.SwitchModels import WaterSpray
from models.managers.ManagerBase import ManagerBase
from models.managers.WaterManager import WaterManager
from utils import str2datetime
from halo import Halo

class SprayManager(ManagerBase):
    def __init__(self, switches: dict, automations: dict, sensors: dict) -> None:
        super().__init__(switches, automations, sensors)
        self.wm = WaterManager(switches, automations, sensors)

        self.waterspray_1: WaterSpray = self._find_switch(name='waterspray_1')
        self.waterspray_2: WaterSpray = self._find_switch(name='waterspray_2')
        self.waterspray_3: WaterSpray = self._find_switch(name='waterspray_3')

        self.spraytime: SprayTime = self._find_automation(name='spraytime')
        self.sprayterm: SprayTerm = self._find_automation(name='sprayterm')

    def check_term(self):
        last_term = (datetime.now() - str2datetime(self.automations['spray_activatedAt'])).total_seconds()/60
        return round(last_term) >= self.sprayterm.period

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
            self.insert_automation_history(subject='waterspray', isCompleted=False)
            self.spray(self.waterspray_1, int(self.spraytime.period))
            self.spray(self.waterspray_2, int(self.spraytime.period) + 1)
            self.spray(self.waterspray_3, int(self.spraytime.period) + 2)
            print("스프레이 자동화 종료됩니다.")
            self.insert_automation_history(subject='waterspray', isCompleted=True)
        else:
            print("스프레이 자동화 작동될 시간이 아닙니다.")