from enum import Enum

# Проблема: Лишние импорты Parrot и ParrotType, так как они уже определены в этом файле.
# Решение: Удалил импорт ненужных классов.

class ParrotType(Enum):
    EUROPEAN = 1
    AFRICAN = 2
    NORWEGIAN_BLUE = 3


class Parrot:

    def __init__(self, type_of_parrot, number_of_coconuts, voltage, nailed):
        self._type = type_of_parrot
        self._number_of_coconuts = number_of_coconuts
        self._voltage = voltage
        self._nailed = nailed

    # Проблема: Нарушение принципа SRP (Single Responsibility Principle) - метод содержит разную логику в зависимости от типа попугая.
    # Решение: Логику можно вынести в отдельные подклассы для каждого типа попугая.
    def speed(self):
        match self._type:  # Проблема: Использование match требует Python 3.10+, что снижает совместимость.
            # Решение: Можно заменить на if-elif для более широкой поддержки.
            case ParrotType.EUROPEAN:
                return self._base_speed()
            case ParrotType.AFRICAN:
                return max(0, self._base_speed() - self._load_factor() * self._number_of_coconuts)
            case ParrotType.NORWEGIAN_BLUE:
                return 0 if self._nailed else self._compute_base_speed_for_voltage(self._voltage)

    # Проблема: Нарушение DRY - метод cry также содержит дублирующуюся логику для типов попугаев.
    # Решение: Использовать паттерн 'Стратегия' или создать подклассы для каждого типа.
    def cry(self):
        match self._type:
            case ParrotType.EUROPEAN:
                return "Sqoork!"
            case ParrotType.AFRICAN:
                return "Sqaark!"
            case ParrotType.NORWEGIAN_BLUE:
                return "Bzzzzzz" if self._voltage > 0 else "..."

    def _compute_base_speed_for_voltage(self, voltage):
        # Проблема: Лишний список в функции min.
        # Решение: Убрал список и передал аргументы напрямую.
        return min(24.0, voltage * self._base_speed())

    def _load_factor(self):
        return 9.0

    def _base_speed(self):
        return 12.0


def test_speed_of_european_parrot():
    parrot = Parrot(ParrotType.EUROPEAN, 0, 0, False)
    assert parrot.speed() == 12.0


def test_cry_of_european_parrot():
    parrot = Parrot(ParrotType.EUROPEAN, 0, 0, False)
    assert parrot.cry() == "Sqoork!"


def test_speed_of_african_parrot_with_one_coconut():
    parrot = Parrot(ParrotType.AFRICAN, 1, 0, False)
    assert parrot.speed() == 3.0


def test_cry_of_african_parrot():
    parrot = Parrot(ParrotType.AFRICAN, 1, 0, False)
    assert parrot.cry() == "Sqaark!"


def test_speed_of_african_parrot_with_two_coconuts():
    parrot = Parrot(ParrotType.AFRICAN, 2, 0, False)
    assert parrot.speed() == 0.0


def test_speed_of_african_parrot_with_no_coconuts():
    parrot = Parrot(ParrotType.AFRICAN, 0, 0, False)
    assert parrot.speed() == 12.0


def test_speed_norwegian_blue_parrot_nailed():
    parrot = Parrot(ParrotType.NORWEGIAN_BLUE, 0, 1.5, True)
    assert parrot.speed() == 0.0


def test_speed_norwegian_blue_parrot_not_nailed():
    parrot = Parrot(ParrotType.NORWEGIAN_BLUE, 0, 1.5, False)
    assert parrot.speed() == 18.0


def test_speed_norwegian_blue_parrot_not_nailed_high_voltage():
    parrot = Parrot(ParrotType.NORWEGIAN_BLUE, 0, 4, False)
    assert parrot.speed() == 24.0


def test_cry_norwegian_blue_parrot_high_voltage():
    parrot = Parrot(ParrotType.NORWEGIAN_BLUE, 0, 4, False)
    assert parrot.cry() == "Bzzzzzz"


def test_cry_norwegian_blue_parrot_no_voltage():
    parrot = Parrot(ParrotType.NORWEGIAN_BLUE, 0, 0, False)
    assert parrot.cry() == "..."
