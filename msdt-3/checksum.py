import json
import hashlib
from typing import List
# we use csv module for working with csv file (не может быть)
import csv
from validator import Validator

CSV_PATH = "19.csv"
JSON_PATH="result.json"
OPTION = 19

"""
В этом модуле обитают функции, необходимые для автоматизированной проверки результатов ваших трудов.
"""
def get_numbers_id_with_wrong_data(csv_file_path: str) -> list[int]:
    """Get numbers with mistake from csv file.

    Args:
        csv_file_path (str): path for csv file for data validating

    Returns:
        list[int]: return list with id with wrong data

    """
    numbers_id_with_wrong_data = []
    validator = Validator()
    with open(CSV_PATH, newline='', encoding="utf-16") as csv_file:
        reader= csv.DictReader(csv_file, delimiter=';')
        for row_id, row in enumerate(reader):
            for pattern, data in row.items():
                if not validator.validate_data(pattern, data):
                    numbers_id_with_wrong_data.append(row_id - 1)

    return numbers_id_with_wrong_data


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
    """Метод для сериализации результатов лабораторной пишите сами.
    Вам нужно заполнить данными - номером варианта и контрольной суммой - файл,
    лежащий в папке с лабораторной.
    
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
    with open(JSON_PATH, "w", encoding="utf-8") as json_file:
        json.dump(result, json_file)


def main():
    # get hash
    numbers_id_with_wrong_data = get_numbers_id_with_wrong_data(CSV_PATH)
    check_sum = calculate_checksum(numbers_id_with_wrong_data)
    serialize_result(OPTION, check_sum)


if __name__ == "__main__":
    main()
