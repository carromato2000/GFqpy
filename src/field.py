from abc import abstractmethod
from src import Ring, RingElement

class Field(Ring):
    pass

class FieldElement(RingElement):
    @abstractmethod
    def __init__(self, field: Field):
        self.field = field

    @abstractmethod
    def __truediv__(self, other):
        pass

    @property
    @abstractmethod
    def inverse():
        pass