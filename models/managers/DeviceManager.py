from abc import abstractmethod
import json
from config import ON, OFF
from db import MysqlController
from logger import logger
from models.Mqtt import MQTT
from models.SwitchModels import SwitchBase

class DeviceManager(MQTT, MysqlController):
    def __init__(self) -> None:
        MysqlController.__init__(self)
        MQTT.__init__(self)
        self.machine_name = None
        self.sw: SwitchBase = None
        self.last_automation = None
        self.state = None
        self.status = None
        self.topic = None
        self.machine_name = ''

    def check_machine_on(self, machine_power):
        return machine_power == 1

    @abstractmethod
    def check_condition(self):
        pass
    
    async def control(self):
        if not self.last_automation['active']:
            logger.info('Automation Inactivated')

        elif self.check_condition() and not self.check_machine_on(self.status):
            await self.sw.on()

        elif not self.check_condition() and self.check_machine_on(self.status):
            await self.sw.off()

        else:
            logger.maintain(f'{self.machine_name} 현상 유지')