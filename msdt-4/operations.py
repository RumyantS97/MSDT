import math
from log_settings import logger


def add(x, y):
    logger.debug(f'Вызвана функция add({x}, {y})')
    return x + y


def subtract(x, y):
    logger.debug(f'Вызвана функция subtract({x}, {y})')
    return x - y


def multiply(x, y):
    logger.debug(f'Вызвана функция multiply({x}, {y})')
    return x * y


def divide(x, y):
    logger.debug(f'Вызвана функция multiply({x}, {y})')
    if y == 0:
        logger.warning("Ошибка деления на ноль!")
        return "Ошибка: деление на ноль!"
    return x / y


def power(x, y):
    logger.debug(f'Вызвана функция power({x}, {y})')
    return x ** y


def sin(x):
    logger.debug(f'Вызвана функция sin({x})')
    return math.sin(math.radians(x))  # Преобразуем градусы в радианы


def cos(x):
    logger.debug(f'Вызвана функция cos({x})')
    return math.cos(math.radians(x))  # Преобразуем градусы в радианы


def tan(x):
    logger.debug(f'Вызвана функция tan({x})')
    return math.tan(math.radians(x))  # Преобразуем градусы в радианы


def sqrt(x):
    logger.debug(f'Вызвана функция sqrt({x})')
    return math.sqrt(x)