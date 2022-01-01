from api import post_report
from config import WATERTANK_HEIGHT


class AutoControl:
    def __init__(self, switches: dict, automations: dict, sensors: dict) -> None:
        self.switches = switches
        self.automations = automations
        self.sensors = sensors

    def _find_switch(self, name):
        return self.switches[name]()

    def _find_automation(self, name):
        return self.automations[name]()

    def _find_sensor(self, name):
        return self.sensors[name]()

    def _set_water_switches(self):
        self.waterpump_center = self._find_switch(name='waterpump_center')
        self.valve_in = self._find_switch(name='valve_in')
        self.valve_out = self._find_switch(name='valve_out')
        self.waterpump_a = self._find_switch(name='waterpump_a')
        self.waterpump_b = self._find_switch(name='waterpump_b')

    def _set_water_automation(self):
        self.watersupply = self._find_automation(name='watersupply')
        self.nutrientsupply = self._find_automation(name='nutrientsupply')

    def _set_water_sensor(self):
        self.waterlevel = self._find_sensor(name='waterlevel')
        self.vi_current = self._find_sensor(name='vi_current')
        self.vo_current = self._find_sensor(name='vo_current')
        self.wpa_current = self._find_sensor(name='wpa_current')
        self.wpb_current = self._find_sensor(name='wpb_current')

    def _set_spray_switches(self):
        self.valve_1 = self._find_switch(name='valve_1')
        self.valve_2 = self._find_switch(name='valve_2')
        self.valve_3 = self._find_switch(name='valve_3')
        self.waterpump_sprayer = self._find_switch(name='waterpump_sprayer')

    def _set_spray_automation(self):
        self.spraytime = self._find_automation(name='spraytime')
        self.sprayterm = self._find_automation(name='sprayterm')

    def _set_spray_sensor(self):
        self.v1_current = self._find_sensor(name='v1_current')
        self.v2_current = self._find_sensor(name='v2_current')
        self.v3_current = self._find_sensor(name='v3_current')
        self.wps_current = self._find_sensor(name='wps_current')

    def control_water(self):
        self._set_water_switches()
        self._set_water_automation()
        self._set_water_sensor()

        waterlevel = self.waterlevel.get_waterlevel()
        if waterlevel < 0:
            post_report(lv=3, problem="수위센서측정에 문제가 생겼습니다.")
            raise Exception('수위센서측정에 문제가 생겼습니다.')
        if  waterlevel <= WATERTANK_HEIGHT * 0.2:
            # 물 다시 채우고 양액 채우기
            pass

    def control_spray(self):
        self._set_spray_switches()
        self._set_spray_automation()
        self._set_spray_sensor()


