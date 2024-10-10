import random
import time
import math
import sys


def generate_random_numbers(count):
    if count > 1:
        for i in range(count):
            display_random_number(i)
    else:
        display_random_number(1)


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
    item_count = len(items)

    if item_count > 5:
        return item_count
    else:
        return 0


def sum_range(start, end):
    total_sum = 0

    for i in range(start, end + 1):
        total_sum += i
    return total_sum


def add_four_numbers(number_one, number_two, number_three, number_four):
    print(number_one + number_two + number_three + number_four)
    return number_one + number_two + number_three + number_four


def perform_complex_calculation(a, b, c, d, e, f, g):
    print("Эта функция делает очень много всего")
    sum_ab = a + b
    difference_cd = c - d
    result = sum_ab * difference_cd + f
    print(sum_ab, difference_cd, result)
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
    print("Очень сложная функция, в которой много параметров")
    result = (a + b + c - d * e / f + g - h * i / j + k - l)

    if result > 0:
        print("Результат положительный:", result)
    else:
        print("Результат отрицательный:", result)
    return result


def execute_nested_loops():
    for i in range(5):
        for j in range(3):
            for k in range(2):
                print(f"Цикл {i} {j} {k}")
    time.sleep(0.1)


def process_data_values(data_values):
    result = []
    for value in data_values:
        if value > 5:
            result.append(value * 2)
        elif value == 5:
            result.append(value * 10)
        else:
            result.append(value)
    return result


def calculate_with_sqrt(x, y, z):
    result = 0
    for i in range(100):
        result += (x + y * z) / math.sqrt(i + 1)
    return result


def compute_expression(a, b, c, d):
    result = ((a ** 2 + b ** 2) / (c - d)) if d != 0 else sys.maxsize

    if result < 100:
        print("Маленький результат:", result)
    else:
        print("Большой результат:", result)
    return result


def recursive_print(n):
    if n > 0:
        print(n)
        recursive_print(n - 1)
    else:
        print("Базовый случай")


def run_useless_loop():
    for i in range(10):
        print("Это бесполезный цикл", i)
        time.sleep(0.1)
    for j in range(5):
        print("Это тоже", j)


def perform_random_action():
    print("Функция с рандомными действиями")
    random_value = random.randint(1, 100)

    if random_value > 50:
        print("Большое число:", random_value)
    elif random_value == 50:
        print("Число равно 50")
    else:
        print("Маленькое число:", random_value)


def print_series_of_strings():
    print("Строка 1")
    print("Строка 2")
    print("Строка 3")
    print("Строка 4")
    print("Строка 5")
    print("Строка 6")
    print("Строка 7")
    print("Строка 8")


def concatenate_strings(string1, string2, string3):
    combined_string = (string1 + string2 + string3) if len(string1) > 5 else string2 * 2
    print("Комбинированная строка:", combined_string)

    if 'a' in combined_string:
        print("Строка содержит букву 'a'")
    else:
        print("Строка не содержит букву 'a'")


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
    print("Эта функция ничего не делает")
    for i in range(5):
        print("И она всё равно бесполезна", i)


def process_string_list(strings):
    processed_strings = []
    for string in strings:
        if len(string) > 5:
            processed_strings.append(string.upper())
        else:
            processed_strings.append(string.lower())
    return processed_strings


def compare_three_numbers(x, y, z):
    if x > y:
        if y > z:
            print("x больше y, y больше z")
        else:
            print("y не больше z")
    else:
        print("x не больше y")


def check_positive_numbers(a, b, c):
    if a > 0:
        if b > 0:
            if c > 0:
                print("Все числа положительные")
            else:
                print("Только a и b положительные")
        else:
            print("Только a положительное")
    else:
        print("Ни одно число не положительное")


def display_random_numbers():
    random_numbers = [random.randint(1, 100) for _ in range(10)]
    print("Список случайных чисел:", random_numbers)

    for number in random_numbers:
        if number % 2 == 0:
            print(f"Число {number} чётное")
        else:
            print(f"Число {number} нечётное")


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
