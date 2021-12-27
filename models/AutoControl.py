
class AutoControl:
    def __init__(self, switches: dict, automations: dict) -> None:
        self.switches = switches
        self.automations = automations

    def _find_switch(self, name):
        return self.switches[name]

    def _find_automation(self, name):
        return self.automations[name]

    def _set_water_switches(self):
        self.waterpump_center = self._find_switch(name='waterpump_center')
        self.valve_in = self._find_switch(name='valve_in')
        self.valve_out = self._find_switch(name='valve_out')
        self.waterpump_a = self._find_switch(name='waterpump_a')
        self.waterpump_b = self._find_switch(name='waterpump_b')

    def _set_water_automation(self):
        self.watersupply = self._find_automation(name='watersupply')
        self.nutrientsupply = self._find_automation(name='nutrientsupply')

    def _set_spray_switches(self):
        self.valve_1 = self._find_switch(name='valve_1')
        self.valve_2 = self._find_switch(name='valve_2')
        self.valve_3 = self._find_switch(name='valve_3')
        self.waterpump_sprayer = self._find_switch(name='waterpump_sprayer')

    def _set_spray_automation(self):
        self.spraytime = self._find_automation(name='spraytime')
        self.sprayterm = self._find_automation(name='sprayterm')

    def control_water(self):
        # TODO : 만약 수위가 매우 낮을 경우 자동으로 물을 채우고 양액을 넣는 자동화
        self._get_water_switches()
        self._get_water_automation()

    def control_spray(self):
        self._get_spray_switches()
        self._get_spray_automation()