

class AutoControl:
    def __init__(self, switches, automations) -> None:
        self.switches = switches
        self.automations = automations

    def _find_switch(self, name):
        return next(item for item in self.switches if item.name == name)

    def _find_automation(self, name):
        return next(item for item in self.automations if item.get_name() == name)

    def control_water(self):
        # TODO : 만약 수위가 매우 낮을 경우 자동으로 물을 채우고 양액을 넣는 자동화
        waterpump_center = self._find_switch(name='waterpump_center')
        valve_in = self._find_switch(name='valve_in')
        valve_out = self._find_switch(name='valve_out')
        watersupply = self._find_automation(name='watersupply')
        nutrientsupply = self._find_automation(name='nutrientsupply')

    def control_nutrient(self):
        """
            waterpump_sprayer <createdAt> createdBy 'auto'
            valve_1 & valve_2 & valve_3
        """
        valve_1 = self._find_switch(name='valve_1')
        valve_2 = self._find_switch(name='valve_2')
        valve_3 = self._find_switch(name='valve_3')
        waterpump_sprayer = self._find_switch(name='waterpump_sprayer')
        spraytime = self._find_automation(name='spraytime')
        sprayterm = self._find_automation(name='sprayterm')
