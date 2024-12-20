import json
import hashlib
import re
import csv
from typing import List

from constants import REGEX, CSV_PATH, RESULT


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


def serialize_result(variant: int, checksum: str, path: str) -> None:
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
        "variant" : variant,
        "checksum": checksum
    }
    with open(path, 'w', encoding='utf-8') as data:
        json.dump(result, data)
    

def read_csv(path: str) -> list[list[str]]:
    """
    read csv file
    """
    data = []
    with open(path, "r", encoding="utf-16") as file:
        file_reader = csv.reader(file, delimiter=';')
        next(file_reader, None)
        for row in file_reader:
            data.append(row)
        return data
    

def invalide_rows(data: list[list[str]], regular: dict) -> list[int]:
    """
    validate rows in a dataset against a set of regular expression patterns
    """
    invalid_rows = []
    for number, row in enumerate(data):
        for _, (field, key) in enumerate(zip(row, regular.keys())):
            pattern = regular[key]
            if not re.fullmatch(pattern, field):
                invalid_rows.append(number)
                break
    return invalid_rows


if __name__ == "__main__":
    csv_data = read_csv(CSV_PATH)
    invalide_index = invalide_rows(csv_data, REGEX)
    result = calculate_checksum(invalide_index)
    serialize_result(13, result, RESULT)
    print(len(invalide_index))
    