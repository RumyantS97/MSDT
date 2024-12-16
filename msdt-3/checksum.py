import csv
import json
import re
from typing import List
import hashlib

"""
В этом модуле обитают функции, необходимые для автоматизированной проверки результатов ваших трудов.
"""

# Регулярные выражения для проверки данных
PATTERNS = {
    "email"         : r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$",
    "height"        : r"^(0\.[5-9][0-9]|[1-2]\.[0-9]{2})$",
    "snils"         : r"^\d{11}$",
    "passport"      : r"^\d{2} \d{2} \d{6}$",
    "occupation"    : r"^[\u0410-\u044f\w\s-]+$",
    "longitude"     : r"^-?\d{1,3}\.\d+$",
    "hex_color"     : r"^#[0-9a-fA-F]{6}$",
    "issn"          : r"^\d{4}-\d{4}$",
    "locale_code"   : r"^[a-z]{2}(-[a-z]{2})?$",
    "time"          : r"^(2[0-3]|[01]?\d):[0-5]?\d:[0-5]?\d(\.\d+)?$"
}


def calculate_checksum(row_numbers: List[int]) -> str:
    """
    Вычисляет md5 хеш от списка целочисленных значений.

    :param row_numbers: список целочисленных номеров строк csv-файла, на которых были найдены ошибки валидации
    :return: md5 хеш для проверки через github action
    """
    row_numbers.sort()
    return hashlib.md5(json.dumps(row_numbers).encode('utf-8')).hexdigest()


def serialize_result(variant: int, checksum: str) -> None:
    """
    Метод для сериализации результатов лабораторной.

    :param variant: номер вашего варианта
    :param checksum: контрольная сумма, вычисленная через calculate_checksum()
    """
    result = {
        "variant": variant,
        "checksum": checksum
    }
    with open("result.json", "w", encoding="utf-8") as result_file:
        json.dump(result, result_file, ensure_ascii=False, indent=4)

def validate_field(field_name: str, value: str) -> bool:
    """
    Проверяет значение поля на валидность по регулярному выражению.

    :param field_name: Название поля
    :param value: Значение поля
    :return: True, если значение валидно, иначе False
    """
    pattern = PATTERNS.get(field_name)
    if pattern:
        return re.match(pattern, value) is not None
    return False

def validate_csv(file_path: str) -> List[int]:
    """
    Проверяет CSV-файл на наличие ошибок.

    :param file_path: Путь к файлу
    :return: Список номеров строк с ошибками
    """
    error_rows = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row_num, row in enumerate(reader):
            adjusted_row_num = row_num - 1
            for field, value in row.items():
                if field in PATTERNS and not validate_field(field, value):
                    error_rows.append(adjusted_row_num)
                    break
    return error_rows

def main():
    csv_file_path = "35.csv"
    variant = 35

    # Валидация и подсчет контрольной суммы
    error_rows = validate_csv(csv_file_path)
    checksum = calculate_checksum(error_rows)

    # Сериализация результатов
    serialize_result(variant, checksum)


if __name__ == "__main__":
    main()