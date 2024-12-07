from enum import Enum

class ParrotType(Enum):
    EUROPEAN = 1
    AFRICAN = 2
    NORWEGIAN_BLUE = 3

class Parrot:

    #def __init__(self, type_of_parrot, number_of_coconuts, voltage, nailed):
     #   self._type = type_of_parrot
      #  self._number_of_coconuts = number_of_coconuts


    def _base_speed(self):
        return 12.0