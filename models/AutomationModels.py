from utils import fDBDate


class AutomationBase:
    def __init__(self, id: int, createdAt: str, name: str) -> None:
        self.id = id
        self.createdAt = fDBDate(createdAt)
        self.name = name

    @classmethod
    def get_name(cls):
        return cls.__name__.lower()


class QuantityModel(AutomationBase):
    def __init__(self, id: int, quantity: int, createdAt: str, name: str) -> None:
        super().__init__(id, createdAt, name)
        self.quantity = quantity

    def get(self):
        return self.quantity

    def pprint(self):
        print({
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity,
            'createdAt': self.createdAt
        })

class PeriodModel(AutomationBase):
    def __init__(self, id: int, period: int, createdAt: str, name: str) -> None:
        super().__init__(id, createdAt, name)
        self.period = period

    def get(self):
        return self.period

    def pprint(self):
        print({
            'id': self.id,
            'name': self.name,
            'period': self.period,
            'createdAt': self.createdAt
        })

class NutrientSupply(QuantityModel):
    def __init__(self, id: int, quantity: int, createdAt: str, name: str) -> None:
        super().__init__(id, quantity, createdAt, name)

class WaterSupply(QuantityModel):
    def __init__(self, id: int, quantity: int, createdAt: str, name: str) -> None:
        super().__init__(id, quantity, createdAt, name)


class SprayTime(PeriodModel):
    def __init__(self, id: int, period: int, createdAt: str, name: str) -> None:
        super().__init__(id, period, createdAt, name)


class SprayTerm(PeriodModel):
    def __init__(self, id: int, period: int, createdAt: str, name: str) -> None:
        super().__init__(id, period, createdAt, name)


