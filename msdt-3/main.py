import csv
import re

from checksum import calculate_checksum, serialize_result
from const import CSV_FILE, PATTERNS, VARIANT


def read_csv(file_name: str) -> list:
    """
    Метод для чтения данных из CSV файла.
    """
    data = []
    with open(file_name, "r", newline="", encoding="utf-16") as file:
        reader = csv.reader(file, delimiter=";")
        for i in reader:
            data.append(i)
        data.pop(0)
        return data


def is_row_valid(row: list) -> bool:
    """
    Проверяет, что каждая строка в данных соответствует регулярным выражениям для каждой колонки.
    """
    for idx, value in enumerate(row):
        pattern = list(PATTERNS.values())[idx]
        if not re.match(pattern, value):
            return False
    return True


def get_invalid_rows(data: list) -> list:
    """
    Метод для поиска индексов невалидных строк в данных.
    """
    invalid_indices = []
    for i, row in enumerate(data):
        if not is_row_valid(row):
            invalid_indices.append(i)
    return invalid_indices


if __name__ == "__main__":
    data = read_csv(CSV_FILE)
    invalid_indices = get_invalid_rows(data)
    checksum = calculate_checksum(invalid_indices)
    serialize_result(VARIANT, checksum)
    print(len(invalid_indices))
