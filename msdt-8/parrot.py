from abc import ABC, abstractmethod

class Parrot(ABC):
    @abstractmethod
    def speed(self):
        pass

    @abstractmethod
    def cry(self):
        pass

    def _base_speed(self):
        return 12.0