from parrot import Parrot, ParrotType

def create_parrot(type_of_parrot, number_of_coconuts, voltage, nailed):
    match type_of_parrot:
        case ParrotType.EUROPEAN:
            parrot = EuropeanParrot(ParrotType.EUROPEAN, number_of_coconuts, voltage, nailed)
        case ParrotType.AFRICAN:
            parrot = AfricanParrot(ParrotType.AFRICAN, number_of_coconuts, voltage, nailed)
        case ParrotType.NORWEGIAN_BLUE:
            parrot = NorwegianBlueParrot(ParrotType.NORWEGIAN_BLUE, number_of_coconuts, voltage, nailed)

    return parrot

class EuropeanParrot(Parrot):
    def __init__(self, type_of_parrot, number_of_coconuts, voltage, nailed):
        super().__init__(type_of_parrot, number_of_coconuts, voltage, nailed)

    def speed(self):
        return self._base_speed()

    def cry(self):
        return "Sqoork!"

class AfricanParrot(Parrot):
    def __init__(self, type_of_parrot, number_of_coconuts, voltage, nailed):
        super().__init__(type_of_parrot, number_of_coconuts, voltage, nailed)

    def speed(self):
        return max(0, self._base_speed() - self._load_factor() * self._number_of_coconuts)

    def cry(self):
        return "Sqaark!"

    def _load_factor(self):
        return 9.0

class NorwegianBlueParrot(Parrot):
    def __init__(self, type_of_parrot, number_of_coconuts, voltage, nailed):
        super().__init__(type_of_parrot, number_of_coconuts, voltage, nailed)

    def speed(self):
        return 0 if self._nailed else self._compute_base_speed_for_voltage(self._voltage)

    def cry(self):
        return "Bzzzzzz" if self._voltage > 0 else "..."

    def _compute_base_speed_for_voltage(self, voltage):
        return min([24.0, voltage * self._base_speed()])