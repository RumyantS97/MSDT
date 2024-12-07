from enum import Enum
from parrot_classes import EuropeanParrot, AfricanParrot, NorwegianBlueParrot

class ParrotType(Enum):
    EUROPEAN = 1
    AFRICAN = 2
    NORWEGIAN_BLUE = 3

def create_parrot(type_of_parrot, number_of_coconuts, voltage, nailed):
    match type_of_parrot:
        case ParrotType.EUROPEAN:
            parrot = EuropeanParrot()
        case ParrotType.AFRICAN:
            parrot = AfricanParrot(number_of_coconuts)
        case ParrotType.NORWEGIAN_BLUE:
            parrot = NorwegianBlueParrot(voltage, nailed)

    return parrot