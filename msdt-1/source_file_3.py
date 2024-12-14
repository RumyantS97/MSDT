# Функция вывода информации по лабораторной работе
def task():
    print("Лабораторная работа №4")
    print("Вариант №3. Выполнил студент группы 6102-020302D Васильев А.Л.")
    print("Задание:")
    print("Алгоритм вычисления функции F(n), где n - натуральное число, задан следующими соотношениями:")
    print("F(n) = 1, при n < 2,")
    print("F(n) = F(n // 2) + 1, когда n >= 2 и чётное,")
    print("F(n) = F(n - 3) + 3, когда n >= 2 и нечётное.")
    print("Напишите программу, которая вычисляет:")
    print("1. Количество значений n на отрезке [1; 100000], для которых F(n) равно 12.")
    print("2. Количество четных цифр результата вычисления F(x), где x - число, заданное пользователем.")
    print("")

# Функция для рекурсии F(n)
def recursive_function(n):
    if (n < 2):
        return 1
    elif (n % 2 == 0):
        return (recursive_function(n // 2) + 1)
    else:
        return (recursive_function(n - 3) + 3)

# Функция для подсчета значений n
def number_of_values_n(count):
    for i in range(1, 101):
        if (recursive_function(i) == 12):
            count += 1
    return count

# Функция для подсчета количества четных цифр
def number_of_even_digits(x):
    if (x < 10):
        if (x % 2 == 0):
            return 1
        else:
            return 0
    else:
        return (number_of_even_digits(x // 10) + number_of_even_digits(x % 10))

# Функция main

task()

flagIn = True
while flagIn:
    print("\nВведите натуральное число:")
    x = int(input("x = "))
    if (x > 0):
        flagIn = False
        print("\nИдёт вычисление...")
        print("\nКоличество значений n на отрезке [1; 100000], для которых F(n) равно 12, равно: ", number_of_values_n(0))
        print("\nКоличество четных цифр результата вычисления F(x) = {1}, где x = {0}, составляет: {2}".format(x, recursive_function(x), number_of_even_digits(recursive_function(x))))
        print("\nКонец работы программы!")
    else:
        print("\nОшибка ввода! Попробуйте снова!")