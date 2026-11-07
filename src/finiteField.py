from abc import abstractmethod
from src import Field, FieldElement

class FiniteField(Field):
    @property
    @abstractmethod
    def order():
        pass

class FiniteFieldElement(FieldElement):
    @property
    def order():
        pass
