from abc import ABC, abstractmethod

class Ring(ABC):
    @property
    @abstractmethod
    def one(self):
        pass

    @property
    @abstractmethod
    def characteristic(self):
        pass

    @abstractmethod
    def compatible(self, other : 'Ring') -> bool:
        pass

    @abstractmethod
    def convert(self, item):
        pass

class RingElement(ABC):
    def __init__(self, ring: Ring, value=None):
        self.ring = ring

    @abstractmethod
    def __add__(self, other):
        pass

    @abstractmethod
    def __radd__(self, other):
        

    @abstractmethod
    def __sub__(self, other):
        pass

    def __rsub__(self, other):
        return -self + other

    @abstractmethod
    def __mul__(self, other):
        pass

    @abstractmethod
    def __rmul__(self, other):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __ne__(self, other):
        pass
    
    @abstractmethod
    def __neg__(self):
        pass

class IntegerRing:
    @property
    def one(self):
        return 1

    @property
    def characteristic(self):
        return 0

    # Definicion de compatibilidad:
    # Un anillo B es compatible con un anillo A si podemos definir la operacion b*a y a*b
    # Mediante un morfismo de anillos de A a B
    # De esta manera, todo anillo es compatible con el anillo de enteros
    # Y el anillo de enteros solo es compatible consigo mismo
    def compatible(self, other: 'Ring') -> bool:
        return isinstance(other, IntegerRing)

    def convert(self, item):
        return item if isinstance(item, int) else None
