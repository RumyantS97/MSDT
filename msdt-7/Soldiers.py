from MilitaryUnitsable import MilitaryUnitsable

class Soldiers(MilitaryUnitsable):
    # Конструктор без параметров
    def __init__(self, name=None, civil=None, num=None, soldiers_array=None):
        if name is None and civil is None and num is None and soldiers_array is None:
            # Конструктор без параметров
            self.name_division = "Пехота"
            self.civil_personnel = 3
            self.number_soldiers = [10 * (i + 1) for i in range(5)]
        elif name is None and civil is None and num is not None:
            # Конструктор для демонстрационной работы с потоками
            self.name_division = "Военная кафедра"
            self.civil_personnel = 1
            self.number_soldiers = [0] * num
        elif name is not None and civil is not None and soldiers_array is not None:
            # Конструктор с параметрами
            if not name:
                raise ValueError("\n\u001B[31mНазвание подразделения не может быть пустым!\u001B[0m")
            self.name_division = name

            if civil <= 0:
                raise ValueError("\n\u001B[31mКоличество гражданского персонала должно быть положительным!\u001B[0m")
            self.civil_personnel = civil

            if len(soldiers_array) == 0:
                raise ValueError("\n\u001B[31mМассив солдат не может быть пустым!\u001B[0m")
            self.number_soldiers = [max(civil, s) for s in soldiers_array]
        else:
            raise ValueError("Некорректные параметры конструктора.")

    # Метод для получения длины массива
    def length(self):
        return len(self.number_soldiers)

    # Установка нового значения в массиве number_soldiers
    def set_number_units(self, index, num):
        if index < 0 or index >= len(self.number_soldiers):
            raise IndexError("\n\u001B[31mОшибка! Выход индекса за диапазон массива!\u001B[0m")
        if num < self.civil_personnel:
            raise ValueError("\n\u001B[31mОшибка! Количество солдат должно быть не меньше гражданского персонала!\u001B[0m")
        self.number_soldiers[index] = num

    # Получение значения из массива number_soldiers
    def get_number_units(self, index):
        if index < 0 or index >= len(self.number_soldiers):
            raise IndexError("\n\u001B[31mОшибка! Выход индекса за диапазон массива!\u001B[0m")
        return self.number_soldiers[index]

    # Установка названия подразделения
    def set_name(self, name):
        if not name:
            raise ValueError("\n\u001B[31mНазвание подразделения не может быть пустым!\u001B[0m")
        self.name_division = name

    # Получение названия подразделения
    def get_name(self):
        return self.name_division

    # Установка количества гражданского персонала
    def set_civil(self, civil):
        if civil <= 0:
            raise ValueError("\n\u001B[31mКоличество гражданского персонала должно быть положительным!\u001B[0m")
        for soldiers in self.number_soldiers:
            if soldiers < civil:
                raise ValueError(f"\n\u001B[31mНовое количество гражданского персонала ({civil}) превышает количество солдат ({soldiers}) в одной из частей!\u001B[0m")
        self.civil_personnel = civil

    # Получение количества гражданского персонала
    def get_civil(self):
        return self.civil_personnel

    # Подсчет общего количества солдат без учета гражданского персонала
    def total_number(self):
        total = 0
        for soldiers in self.number_soldiers:
            if soldiers <= 0:
                raise ValueError("\n\u001B[31mВ массиве содержатся некорректные данные!\u001B[0m")
            total += soldiers - self.civil_personnel
        return total