import json
import hashlib
from typing import List

from Validator import Validator

# For work with csv files
import csv

"""
В этом модуле обитают функции, необходимые для автоматизированной проверки результатов ваших трудов.
"""

CSV_PATH = "./29.csv"
JSON_PATH = "./result.json"
OPTION = 29


def get_rows_with_invalid_data(csv_path: str) -> list:
    validator = Validator()
    counter = 0
    rows_with_invalid_data = []

    # Open csv file
    with open(csv_path, encoding="utf-16") as csv_file:
        # Skip first row (headers row)
        next(csv_file)
        csv_reader = csv.reader(csv_file, delimiter=",")
        # While row in file:
        for row in csv_reader:
            # Read row
            data = row[0].split(";")
            if len(data) != 10:
                rows_with_invalid_data.append(counter)
                counter += 1
                continue
            email = data[0]
            http_status = data[1][1:-1]
            inn = data[2][1:-1]
            passport = data[3][1:-1]
            ipv4 = data[4][1:-1]
            latitude = data[5][1:-1]
            hex_color = data[6][1:-1]
            isbn = data[7][1:-1]
            uuid = data[8][1:-1]
            time = data[9][1:-1]
            # Validate row
            # If mistake:
            if (
                not validator.is_email_valid(email)
                or not validator.is_http_status_valid(http_status)
                or not validator.is_inn_valid(inn)
                or not validator.is_passport_valid(passport)
                or not validator.is_ipv4_valid(ipv4)
                or not validator.is_latitude_valid(latitude)
                or not validator.is_rgb_valid(hex_color)
                or not validator.is_isbn_valid(isbn)
                or not validator.is_uuid_valid(uuid)
                or not validator.is_time_valid(time)
            ):
                # write row number
                rows_with_invalid_data.append(counter)
            counter += 1
            # else:
            # skip

        # return row number list
        return rows_with_invalid_data


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
    return hashlib.md5(json.dumps(row_numbers).encode("utf-8")).hexdigest()


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
    with open(JSON_PATH, "r") as json_file:
        data = json.load(json_file)
    data["variant"] = variant
    data["checksum"] = checksum
    with open(JSON_PATH, "w") as json_file:
        json.dump(data, json_file)


row_numbers = get_rows_with_invalid_data(CSV_PATH)
sha256sum = calculate_checksum(row_numbers=row_numbers)
serialize_result(OPTION, sha256sum)
