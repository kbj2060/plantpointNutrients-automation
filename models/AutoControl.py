class AutoControl:
    def __init__(self, switches: dict, automations: dict, sensors: dict) -> None:
        self.switches = switches
        self.automations = automations
        self.sensors = sensors

    def _find_switch(self, name):
        return self.switches[name]

    def _find_automation(self, name):
        return self.automations[name]

    def control_water(self):
        watersupply = self._find_automation(name='watersupply')
        nutrientsupply = self._find_automation(name='nutrientsupply')
        valve_1 = self._find_switch(name='valve_1')
        valve_2 = self._find_switch(name='valve_2')
        valve_3 = self._find_switch(name='valve_3')
        waterpump_sprayer = self._find_switch(name='waterpump_sprayer')
        # TODO : 만약 수위가 매우 낮을 경우 자동으로 물을 채우고 양액을 넣는 자동화

    def control_spray(self):
        waterpump_center = self._find_switch(name='waterpump_center')
        valve_in = self._find_switch(name='valve_in')
        valve_out = self._find_switch(name='valve_out')
        waterpump_a = self._find_switch(name='waterpump_a')
        waterpump_b = self._find_switch(name='waterpump_b')
        spraytime = self._find_automation(name='spraytime')
        sprayterm = self._find_automation(name='sprayterm')

class AutoContdition:
    def get_waterlevel(self, sensor):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(sensor.pin, GPIO.OUT)
        GPIO.setup(sensor.pin+1, GPIO.IN)  
