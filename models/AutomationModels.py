from datetime import datetime
from utils import fDBDate


class AutomationBase:
    def __init__(self, id: int, createdAt: datetime) -> None:
        self.id = id
        # self.createdAt = fDBDate(createdAt)
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

    def pprint(self):
        print({
            'id': self.id,
            'quantity': self.quantity,
            'createdAt': self.createdAt
        })

class PeriodModel(AutomationBase):
    def __init__(self, id: int, period: int, createdAt: datetime) -> None:
        super().__init__(id, createdAt)
        self.period = period

    def get(self):
        return self.period

    def pprint(self):
        print({
            'id': self.id,
            'period': self.period,
            'createdAt': self.createdAt
        })

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

class WaterSupply(QuantityModel):
    def __init__(self, id: int, quantity: int, createdAt: str) -> None:
        super().__init__(id, quantity, createdAt)

class SprayTime(PeriodModel):
    def __init__(self, id: int, period: int, createdAt: str) -> None:
        super().__init__(id, period, createdAt)

class SprayTerm(PeriodModel):
    def __init__(self, id: int, period: int, createdAt: str) -> None:
        super().__init__(id, period, createdAt)

class AutomationLed(RangeModel):
    def __init__(self, id: int, start: int, end: int, active: bool, createdAt: datetime) -> None:
        super().__init__(id, start, end, active, createdAt)

class AutomationAC(RangeModel):
    def __init__(self, id: int, start: str, end: str, active: bool, createdAt: datetime) -> None:
        super().__init__(id, start, end, active, createdAt)

class AutomationFan(TermModel):
    def __init__(self, id: int, term: int, active: bool, createdAt: datetime) -> None:
        super().__init__(id, term, active, createdAt)

class AutomationRoofFan(TermModel):
    def __init__(self, id: int, term: int, active: bool, createdAt: datetime) -> None:
        super().__init__(id, term, active, createdAt)

