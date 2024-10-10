import random
import time
import math
import sys


def generate_random_numbers(count):
    for i in range(max(count, 1)):
        display_random_number(i)


def display_random_number(index):
    random_number = random.randint(1, 100)
    print("Случайное число:", random_number)

    if random_number > 50:
        print(f"Число {random_number} больше 50")
    elif random_number == 50:
        print(f"Число {random_number} равно 50")
    else:
        print(f"Число {random_number} меньше 50")


def get_length_if_greater_than_five(items):
    return len(items) if len(items) > 5 else 0


def sum_range(start, end):
    return sum(range(start, end + 1))


def add_four_numbers(number_one, number_two, number_three, number_four):
    result = number_one + number_two + number_three + number_four
    print(result)
    return result


def perform_complex_calculation(a, b, c, d, e, f, g):
    print("Эта функция делает очень много всего")
    result = (a + b) * (c - d) + f
    print(result)
    return result


class Car:
    def __init__(self, brand, color):
        self.brand = brand
        self.color = color

    def start_engine(self):
        print("Двигатель запущен")

    def drive(self):
        print(f"{self.brand} едет")

    def stop(self):
        print(f"{self.brand} остановился")


def calculate_large_expression(a, b, c, d, e, f, g, h, i, j, k, l):
    result = (a + b + c - d * e / f + g - h * i / j + k - l)

    print("Результат положительный:", result) if result > 0 else print("Результат отрицательный:", result)
    return result


def execute_nested_loops():
    print("\n".join([f"Цикл {i} {j} {k}" for i in range(5) for j in range(3) for k in range(2)]))
    time.sleep(0.1)


def process_data_values(data_values):
    return [(value * 2 if value > 5 else value * 10 if value == 5 else value) for value in data_values]


def calculate_with_sqrt(x, y, z):
    return sum((x + y * z) / math.sqrt(i + 1) for i in range(100))


def compute_expression(a, b, c, d):
    if d == 0:
        return sys.maxsize
    result = (a ** 2 + b ** 2) / (c - d)
    print("Результат:", "Маленький" if result < 100 else "Большой", result)
    return result


def recursive_print(n):
    while n > 0:
        print(n)
        n -= 1
    print("Базовый случай")


def run_useless_loop():
    for i in range(10):
        print("Это бесполезный цикл", i)
        time.sleep(0.1)

    print("\n".join([f"Это тоже {j}" for j in range(5)]))


def perform_random_action():
    random_value = random.randint(1, 100)
    print("Функция с рандомными действиями")
    print(f"Число равно {random_value}", end=' ')
    if random_value > 50:
        print("— Большое число")
    elif random_value == 50:
        print("— Число равно 50")
    else:
        print("— Маленькое число")


def print_series_of_strings():
    strings = [f"Строка {i}" for i in range(1, 9)]
    print("\n".join(strings))


def concatenate_strings(string1, string2, string3):
    combined_string = string1 + string2 + string3 if len(string1) > 5 else string2 * 2
    print("Комбинированная строка:", combined_string)

    print("Строка содержит букву 'a'") if 'a' in combined_string else print("Строка не содержит букву 'a'")


class Building:
    def __init__(self, floors, color):
        self.floors = floors
        self.color = color

    def describe_building(self):
        print(f"Здание имеет {self.floors} этажей и {self.color} цвет")

    def build_structure(self):
        print(f"Строим здание с {self.floors} этажами")

    def demolish_building(self):
        print("Здание снесено")


def calculate_expression(a, b, c):
    result = (a + b) * (c - b) / (a + 1)
    if result > 1000:
        print("Огромный результат")
    elif result == 1000:
        print("Ровно тысяча")
    else:
        print("Маленький результат")
    return result


def useless_function():
    for i in range(5):
        print("Эта функция ничего не делает", i)


def process_string_list(strings):
    return [string.upper() if len(string) > 5 else string.lower() for string in strings]


def compare_three_numbers(x, y, z):
    if x > y > z:
        print("x больше y, y больше z")
    elif y <= z:
        print("y не больше z")
    else:
        print("x не больше y")


def check_positive_numbers(a, b, c):
    if all(x > 0 for x in [a, b, c]):
        print("Все числа положительные")
    elif a > 0 and b > 0:
        print("Только a и b положительные")
    elif a > 0:
        print("Только a положительное")
    else:
        print("Ни одно число не положительное")


def display_random_numbers():
    random_numbers = [random.randint(1, 100) for _ in range(10)]
    for number in random_numbers:
        print(f"Число {number} {'чётное' if number % 2 == 0 else 'нечётное'}")


def say_goodbye():
    print("Последняя функция в коде")
    time.sleep(1)
    print("Прощай!")


if __name__ == "__main__":
    main()
    calculate_large_expression(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
    execute_nested_loops()
    process_data_values([3, 6, 9, 5, 2])
    calculate_with_sqrt(1, 2, 3)
    compute_expression(10, 20, 5, 2)
    recursive_print(10)
    run_useless_loop()
    perform_random_action()
    print_series_of_strings()
    concatenate_strings("hello", "world", "python")
    building = Building(5, "синий")
    building.describe_building()
    building.build_structure()
    calculate_expression(10, 20, 30)
    useless_function()
    process_string_list(["apple", "banana", "kiwi", "melon", "grape"])
    compare_three_numbers(5, 3, 2)
    check_positive_numbers(1, 2, 3)
    display_random_numbers()
    say_goodbye()
