from datetime import datetime
from utils import fDBDate


class AutomationBase:
    def __init__(self, id: int, createdAt: datetime) -> None:
        self.id = id
        self.createdAt = createdAt

    @classmethod
    def get_name(cls):
        return cls.__name__.lower()


class QuantityModel(AutomationBase):
    def __init__(self, id: int, quantity: int, createdAt: datetime) -> None:
        super().__init__(id, createdAt)
        self.quantity = quantity

    def get(self):
        return self.quantity

class PeriodModel(AutomationBase):
    def __init__(self, id: int, period: int, createdAt: datetime) -> None:
        super().__init__(id, createdAt)
        self.period = period

    def get(self):
        return self.period

class TermModel:
    def __init__(self, id: int, term: int, active: bool, createdAt: datetime) -> None:
        self.id = id
        self.term = term
        self.active = active
        self.createdAt = createdAt

class RangeModel:
    def __init__(self, id: int, start: int or str, end: int or str, active: bool, createdAt: datetime) -> None:
        self.id = id
        self.start = start
        self.end = end
        self.active = active
        self.createdAt = createdAt


class NutrientSupply(QuantityModel):
    def __init__(self, id: int, quantity: int, createdAt: str) -> None:
        super().__init__(id, quantity, createdAt)
        self.name = 'nutrientsupply'

class WaterSupply(QuantityModel):
    def __init__(self, id: int, quantity: int, createdAt: str) -> None:
        super().__init__(id, quantity, createdAt)
        self.name = 'watersupply'

class SprayTime(PeriodModel):
    def __init__(self, id: int, period: int, createdAt: str) -> None:
        super().__init__(id, period, createdAt)
        self.name = 'spraytime'

class SprayTerm(PeriodModel):
    def __init__(self, id: int, period: int, createdAt: str) -> None:
        super().__init__(id, period, createdAt)
        self.name = 'sprayterm'

class AutomationLed(RangeModel):
    def __init__(self, id: int, start: int, end: int, active: bool, createdAt: datetime) -> None:
        super().__init__(id, start, end, active, createdAt)
        self.name = 'automation_led'

class AutomationAC(RangeModel):
    def __init__(self, id: int, start: str, end: str, active: bool, createdAt: datetime) -> None:
        super().__init__(id, start, end, active, createdAt)
        self.name = 'automation_ac'

class AutomationFan(TermModel):
    def __init__(self, id: int, term: int, active: bool, createdAt: datetime) -> None:
        super().__init__(id, term, active, createdAt)
        self.name = 'automation_fan'

class AutomationRoofFan(TermModel):
    def __init__(self, id: int, term: int, active: bool, createdAt: datetime) -> None:
        super().__init__(id, term, active, createdAt)
        self.name = 'automation_rooffan'

