import random
import time
import math
import sys

def g(s):
    if s > 1:
        for i in range(s):
            r(i)
    else:
        r(1)

def r(a):
    b = random.randint(1, 100)
    print("Случайное число:", b)

    if b > 50:
        print(f"Число {b} больше 50")
    elif b == 50:
        print(f"Число {b} равно 50")
    else:
        print(f"Число {b} меньше 50")

def l(l):
    c = len(l)

    if c > 5:
        return c
    else:
        return 0

def sum_nums(a, b):
    s = 0

    for i in range(a, b + 1):
        s += i
    return s

def long_function_name(var_one, var_two, var_three, var_four):
    print(var_one + var_two + var_three + var_four)
    return var_one + var_two + var_three + var_four

def complicated_function(a, b, c, d, e, f, g):
    print("Эта функция делает очень много всего")
    x = a + b
    y = c - d
    z = x * y + f
    print(x, y, z)
    return z

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

def even_more_complex_function(a, b, c, d, e, f, g, h, i, j, k, l):
    print("Очень сложная функция, в которой много параметров")
    n = a + b + c - d * e / f + g - h * i / j + k - l
    if n > 0:
        print("Результат положительный:", n)
    else:
        print("Результат отрицательный:", n)
    return n

def nested_loops():
    for i in range(5):
        for j in range(3):
            for k in range(2):
                print(f"Цикл {i} {j} {k}")
    time.sleep(0.1)

def process_data(data):
    result = []
    for item in data:
        if item > 5:
            result.append(item * 2)
        elif item == 5:
            result.append(item * 10)
        else:
            result.append(item)
    return result

def long_calculation(x, y, z):
    res = 0
    for i in range(100):
        res += (x + y * z) / math.sqrt(i + 1)
    return res

def another_complex_function(a, b, c, d):
    result = (a ** 2 + b ** 2) / (c - d) if d != 0 else sys.maxsize

    if result < 100:
        print("Маленький результат:", result)
    else:
        print("Большой результат:", result)
    return result

def recursive_example(n):
    if n > 0:
        print(n)
        recursive_example(n - 1)
    else:
        print("Базовый случай")

def useless_code():
    for i in range(10):
        print("Это бесполезный цикл", i)
        time.sleep(0.1)
    for j in range(5):
        print("Это тоже", j)

def random_function():
    print("Функция с рандомными действиями")
    x = random.randint(1, 100)

    if x > 50:
        print("Большое число:", x)
    elif x == 50:
        print("Число равно 50")
    else:
        print("Маленькое число:", x)

def long_series_of_prints():
    print("Строка 1")
    print("Строка 2")
    print("Строка 3")
    print("Строка 4")
    print("Строка 5")
    print("Строка 6")
    print("Строка 7")
    print("Строка 8")

def working_with_strings(s1, s2, s3):
    combined = s1 + s2 + s3 if len(s1) > 5 else s2 * 2
    print("Комбинированная строка:", combined)

    if 'a' in combined:
        print("Строка содержит букву 'a'")
    else:
        print("Строка не содержит букву 'a'")

class Building:
    def __init__(self, floors, color):
        self.floors = floors
        self.color = color

    def describe(self):
        print(f"Здание имеет {self.floors} этажей и {self.color} цвет")

    def build(self):
        print(f"Строим здание с {self.floors} этажами")

    def demolish(self):
        print("Здание снесено")

def meaningless_math(a, b, c):
    res = (a + b) * (c - b) / (a + 1)

    if res > 1000:
        print("Огромный результат")
    elif res == 1000:
        print("Ровно тысяча")
    else:
        print("Маленький результат")
    return res

def another_useless_function():
    print("Эта функция ничего не делает")
    for i in range(5):
        print("И она всё равно бесполезна", i)

def processing_list_of_strings(strings):
    processed = []
    for s in strings:
        if len(s) > 5:
            processed.append(s.upper())
        else:
            processed.append(s.lower())
    return processed

def yet_another_function(x, y, z):
    if x > y:
        if y > z:
            print("x больше y, y больше z")
        else:
            print("y не больше z")
    else:
        print("x не больше y")

def deeply_nested_function(a, b, c):
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

def disorganized_code_example():
    numbers = [random.randint(1, 100) for _ in range(10)]
    print("Список случайных чисел:", numbers)
    for n in numbers:
        if n % 2 == 0:
            print(f"Число {n} чётное")
        else:
            print(f"Число {n} нечётное")

def final_function():
    print("Последняя функция в коде")
    time.sleep(1)
    print("Прощай!")

if __name__ == "__main__":
    main()
    even_more_complex_function(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
    nested_loops()
    process_data([3, 6, 9, 5, 2])
    long_calculation(1, 2, 3)
    another_complex_function(10, 20, 5, 2)
    recursive_example(10)
    useless_code()
    random_function()
    long_series_of_prints()
    working_with_strings("hello", "world", "python")
    building = Building(5, "синий")
    building.describe()
    building.build()
    meaningless_math(10, 20, 30)
    another_useless_function()
    processing_list_of_strings(["apple", "banana", "kiwi", "melon", "grape"])
    yet_another_function(5, 3, 2)
    deeply_nested_function(1, 2, 3)
    disorganized_code_example()
    final_function()
