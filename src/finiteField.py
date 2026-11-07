from abc import ABC, abstractmethod
from src import Ring

class Field(ABC, Ring):
    pass

class FiniteField(ABC, Field):
    @property
    @abstractmethod
    def order(self):
        pass

class FiniteFieldElement(ABC):
    def __init__(self, field: FiniteField, value=None):
        self.field = field

    @abstractmethod
    def __add__(self, other):
        pass

    @abstractmethod
    def __sub__(self, other):
        pass

    @abstractmethod
    def __mul__(self, other):
        pass

    @abstractmethod
    def __truediv__(self, other):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __neg__(self):
        pass

    @abstractmethod
    def __pow__(self, exponent):
        pass

    @abstractmethod
    def __order__(self):
        pass
