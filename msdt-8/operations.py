import math


def add(x, y):
    return x + y


def subtract(x, y):
    return x - y


def multiply(x, y):
    return x * y


def divide(x, y):
    if y == 0:
        return "Ошибка: деление на ноль!"
    return x / y


def power(x, y):
    return x ** y


def sin(x):
    return math.sin(math.radians(x))  # Преобразуем градусы в радианы


def cos(x):
    return math.cos(math.radians(x))  # Преобразуем градусы в радианы


def tan(x):
    return math.tan(math.radians(x))  # Преобразуем градусы в радианы

