from parrot import Parrot, ParrotType

def create_parrot(type_of_parrot, number_of_coconuts, voltage, nailed):
    match type_of_parrot:
        case ParrotType.EUROPEAN:
            parrot = EuropeanParrot(type_of_parrot, number_of_coconuts, voltage, nailed)
        case ParrotType.AFRICAN:
            parrot = AfricanParrot(type_of_parrot, number_of_coconuts, voltage, nailed)
        case ParrotType.NORWEGIAN_BLUE:
            parrot = NorwegianBlueParrot(type_of_parrot, number_of_coconuts, voltage, nailed)

    return parrot

class EuropeanParrot(Parrot):
    def __init__(self, type_of_parrot, number_of_coconuts, voltage, nailed):
        super().__init__(type_of_parrot, number_of_coconuts, voltage, nailed)

class AfricanParrot(Parrot):
    def __init__(self, type_of_parrot, number_of_coconuts, voltage, nailed):
        super().__init__(type_of_parrot, number_of_coconuts, voltage, nailed)

class NorwegianBlueParrot(Parrot):
    def __init__(self, type_of_parrot, number_of_coconuts, voltage, nailed):
        super().__init__(type_of_parrot, number_of_coconuts, voltage, nailed)