from abc import abstractmethod, ABCMeta
from utils import fDBDate


class SwitchBase(metaclass=ABCMeta):
    def __init__(self, id: int, name: str, createdAt: str) -> None:
        self.id = id
        self.name = name
        self.createdAt = fDBDate(createdAt)
        self.purpose = self.name.split('_')[1] if '_' in self.name else None
        self.poweredAt = None
        self.status = None
    
    @classmethod
    def get_name(cls):
        return cls.__name__.lower()

    def set_switch_info(self, status, poweredAt):
        self.poweredAt = fDBDate(poweredAt)
        self.status = status

    def on(self):
        self.status = 1

    def off(self):
        self.status = 0

    def pprint(self):
        print({
            'id': self.id,
            'name': self.name,
            'createdAt': self.createdAt,
            'purpose': self.purpose,
            'poweredAt': self.poweredAt,
            'status': self.status
        })


class Valve(SwitchBase):
    pass

class WaterPump(SwitchBase):
    pass

class LED(SwitchBase):
    pass