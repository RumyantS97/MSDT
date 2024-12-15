from MilitaryUnitsable import MilitaryUnitsable

class Aviation(MilitaryUnitsable):
    # Конструктор без параметров
    def __init__(self, name=None, civil=None, num=None, aviation_array=None):
        if name is None and civil is None and num is None and aviation_array is None:
            # Конструктор без параметров
            self.name_aviation = "Истребительная"
            self.civil_aviation = 3
            self.number_aviation = [10 * (i + 1) for i in range(5)]
        elif name is None and civil is None and num is not None:
            # Конструктор для демонстрационной работы с потоками
            self.name_aviation = "Учебная"
            self.civil_aviation = 1
            self.number_aviation = [0] * num
        elif name is not None and civil is not None and aviation_array is not None:
            # Конструктор с параметрами
            if not name:
                raise ValueError("\n\u001B[31mТип авиации не может быть пустым!\u001B[0m")
            self.name_aviation = name

            if civil <= 0:
                raise ValueError("\n\u001B[31mКоличество гражданской авиации не может быть меньше или равно нулю!\u001B[0m")
            self.civil_aviation = civil

            if len(aviation_array) == 0:
                raise ValueError("\n\u001B[31mМассив авиации не может быть пустым!\u001B[0m")
            self.number_aviation = [max(civil, num) for num in aviation_array]
        else:
            raise ValueError("Некорректные параметры конструктора.")

    def length(self):
        return len(self.number_aviation)

    def set_number_units(self, index, num):
        if index < 0 or index >= len(self.number_aviation):
            raise IndexError("\n\u001B[31mОшибка! Выход индекса за диапазон массива!\u001B[0m")
        if num < self.civil_aviation:
            raise ValueError("\n\u001B[31mОшибка! Количество авиации должно быть не меньше количества гражданской авиации на аэродроме!\u001B[0m")
        self.number_aviation[index] = num

    def get_number_units(self, index):
        if index < 0 or index >= len(self.number_aviation):
            raise IndexError("\n\u001B[31mОшибка! Выход индекса за диапазон массива!\u001B[0m")
        return self.number_aviation[index]

    def set_name(self, name):
        if not name:
            raise ValueError("\n\u001B[31mТип авиации не может быть пустым!\u001B[0m")
        self.name_aviation = name

    def get_name(self):
        return self.name_aviation

    def set_civil(self, civil):
        if civil <= 0:
            raise ValueError("\n\u001B[31mКоличество гражданской авиации не может быть меньше или равно нулю!\u001B[0m")
        for aviation in self.number_aviation:
            if aviation < civil:
                raise ValueError(f"\n\u001B[31mНовое количество гражданской авиации ({civil}) превышает количество авиации ({aviation}) на одном из аэродромов!\u001B[0m")
        self.civil_aviation = civil

    def get_civil(self):
        return self.civil_aviation

    def total_number(self):
        total = 0
        for aviation in self.number_aviation:
            total += aviation - self.civil_aviation
        if total < 0:
            raise ValueError("\n\u001B[31mВ массиве содержатся некорректные данные!\u001B[0m")
        return total

    def __str__(self):
        return (f"\nТип авиации: \"{self.name_aviation}\"\n"
                f"Количество гражданской авиации на каждом аэродроме: {self.civil_aviation}\n"
                f"Количество авиации на аэродромах: {' '.join(map(str, self.number_aviation))}")

    def __eq__(self, other):
        if isinstance(other, Aviation):
            return (self.name_aviation == other.name_aviation and
                    self.civil_aviation == other.civil_aviation and
                    self.number_aviation == other.number_aviation)
        return False

    def __hash__(self):
        return hash((self.name_aviation, self.civil_aviation, tuple(self.number_aviation)))
