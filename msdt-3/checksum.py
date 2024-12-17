import json
import hashlib
import csv
import re
from typing import List

import constants

"""
В этом модуле обитают функции, необходимые для автоматизированной проверки результатов ваших трудов.
"""


def calculate_checksum(row_numbers: List[int]) -> str:
    """
    Вычисляет md5 хеш от списка целочисленных значений.

    ВНИМАНИЕ, ВАЖНО! Чтобы сумма получилась корректной, считать, что первая строка с данными csv-файла имеет номер 0
    Другими словами: В исходном csv 1я строка - заголовки столбцов, 2я и остальные - данные.
    Соответственно, считаем что у 2 строки файла номер 0, у 3й - номер 1 и так далее.

    :param row_numbers: список целочисленных номеров строк csv-файла, на которых были найдены ошибки валидации
    :return: md5 хеш для проверки через github action
    """
    row_numbers.sort()
    return hashlib.md5(json.dumps(row_numbers).encode('utf-8')).hexdigest()


def serialize_result(variant: int, checksum: str) -> None:
    """
    Метод для сериализации результатов лабораторной пишите сами.
    Вам нужно заполнить данными - номером варианта и контрольной суммой - файл, лежащий в папке с лабораторной.
    Файл называется, очевидно, result.json.

    ВНИМАНИЕ, ВАЖНО! На json натравлен github action, который проверяет корректность выполнения лабораторной.
    Так что не перемещайте, не переименовывайте и не изменяйте его структуру, если планируете успешно сдать лабу.

    :param variant: номер вашего варианта
    :param checksum: контрольная сумма, вычисленная через calculate_checksum()
    """
    result = {
        "variant": 18,
        "checksum": checksum
    }
    with open(constants.RESULT, 'w', encoding='utf-8') as data:
        json.dump(result, data)


def csv_read(path: str) -> list[list[str]]:
    """
    Чтение csv файла
    """
    with open(path, 'r', encoding='utf-16') as data:
        return [row for row in csv.reader(data, delimiter=";")][1:]
    

def is_valid(regex: dict, row: list[str]) -> bool:
    """
    Проверяет, проходит ли строка регулярные выражения
    """
    return all(re.match(regex[i], data) for i, data in zip(regex.keys(), row))


def invalid_rows(regex: dict, data: list[list[str]]) -> list[int]:
    """
    Находит индексы невалидных строк
    """
    return [i for i, row in enumerate(data) if not is_valid(regex, row)]


if __name__ == "__main__":
    data = csv_read(constants.CSV)
    rows = invalid_rows(constants.REGEX, data)
    checksum = calculate_checksum(rows)
    serialize_result(18, checksum)