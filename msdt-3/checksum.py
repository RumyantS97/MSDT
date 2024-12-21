import json
import re
import csv
import hashlib
from typing import List

from constants import CSV_PATH, REGEX_PATH, RESULT_PATH
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
    pass


def read_json(path: str) -> dict:
    """
    Reads a JSON file and returns its content as a dictionary.
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print('No such file or directory')
    except Exception as e:
        raise e


def read_csv(path: str) -> list[list[str]]:
    """
    Reads a CSV file and returns its content as a list of rows, each represented as a list of strings.
    """
    try:
        file_data = []
        with open(path, "r", encoding="utf-16") as file:
            file_reader = csv.reader(file, delimiter=';')
            next(file_reader, None)
            for row in file_reader:
                file_data.append(row)
            return file_data
    except FileNotFoundError:
        raise FileNotFoundError('No such file or directory')
    except Exception as e:
        raise e


def write_json_file(path: str, data: dict) -> None:
    """
    Writes a dictionary to a JSON file.
    """
    try:
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data, file)
    except FileNotFoundError:
        raise FileNotFoundError('No such file or directory')
    except Exception as e:
        raise e


def validate_data(data: list[list[str]], regex: dict) -> list[int]:
    """
    Checks rows from a CSV file for compliance with regular expressions.
    """
    invalid_rows = []

    for row_number, row in enumerate(data):
        for col_index, (field, key) in enumerate(zip(row, regex.keys())):
            pattern = regex[key]
            if not re.fullmatch(pattern, field):
                invalid_rows.append(row_number)
                break

    return invalid_rows


if __name__ == "__main__":
    data = read_csv(CSV_PATH)
    regex = read_json(REGEX_PATH)
    invalid_rows = validate_data(data, regex)
    summ = calculate_checksum(invalid_rows)
    result = {
        "variant": 94,
        "checksum": summ
    }
    write_json_file(RESULT_PATH, result)

    print(f"Невалидные строки: {invalid_rows}")
    print(f"Контрольная сумма: {summ}")
    print(len(invalid_rows))
