import json
import hashlib
import csv
import re
from typing import List

from setup import CSV_PATH, REGULAR_JSON, RESULT_PATH
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
        "variant": variant,
        "checksum": checksum
    }
    with open(RESULT_PATH, 'w', encoding='utf-8') as file:
        json.dump(result, file)


def read_json(path: str) -> dict:
    """
    Чтение json файла
    """
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


def read_csv(path: str) -> list[list[str]]:
    """
    Чтение csv файлов
    """
    with open(path, 'r', encoding="utf-16") as file:
        return [row for row in csv.reader(file, delimiter=";")][1:]


def validate_data(data: list[list[str]], regular: dict) -> list[int]:
    """
    Поиск индексов невалидных строк
    """
    invalid_rows = []
    for row_number, row in enumerate(data):
        for col_index, (field, key) in enumerate(zip(row, regular.keys())):
            pattern = regular[key]
            if not re.fullmatch(pattern, field):
                invalid_rows.append(row_number)
                break

    return invalid_rows


if __name__ == "__main__":
    regular = read_json(REGULAR_JSON)
    data = read_csv(CSV_PATH)
    indexs = validate_data(data, regular)
    checksum = calculate_checksum(indexs)
    serialize_result(3, checksum)
