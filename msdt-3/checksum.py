import csv
import json
import hashlib
import re
from typing import List

# Регулярные выражения для проверки данных
PATTERNS = {
    "email"                 : r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$",
    "http_status_message"   : r"^\d{3}\s[A-Za-z\s]+$",
    "inn"                   : r"^\d{12}$",
    "passport"              : r"^\d{2}\s\d{2}\s\d{6}$",
    "ip_v4"                 : r"^(25[0-5]|2[0-4]\d|1\d{2}|\d{1,2})\.(25[0-5]|2[0-4]\d|1\d{2}|\d{1,2})\.(25[0-5]"
                              r"|2[0-4]\d|1\d{2}|\d{1,2})\.(25[0-5]|2[0-4]\d|1\d{2}|\d{1,2})$",
    "latitude"              : r"^-?(90(\.0+)?|[1-8]?\d(\.\d+)?)$",
    "hex_color"             : r"^#[0-9a-fA-F]{6}$",
    "isbn"                  : r"^\d{1,5}-\d{1,7}-\d{1,7}-\d{1,7}-\d{1}$",
    "uuid"                  : r"^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$",
    "time"                  : r"^(2[0-3]|[01]?\d):[0-5]?\d:[0-5]?\d(\.\d{1,6})?$"
}

def field_validate(field_name: str, value: str) -> bool:
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

def csv_validate(file_path: str) -> List[int]:
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
                if field in PATTERNS and not field_validate(field, value):
                    error_rows.append(adjusted_row_num)
                    break
    return error_rows

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
    Сериализует результаты в JSON-файл result.json.
    :param variant: номер варианта
    :param checksum: контрольная сумма
    """
    result = {
        "variant": variant,
        "checksum": checksum
    }

    with open("result.json", "w", encoding="utf-8") as result_file:
        json.dump(result, result_file, ensure_ascii=False, indent=4)

def main():
    csv_file_path = "37.csv"
    variant = 37

    # Валидация и подсчет контрольной суммы
    error_rows = csv_validate(csv_file_path)
    checksum = calculate_checksum(error_rows)

    # Сериализация результатов
    serialize_result(variant, checksum)

if __name__ == "__main__":
    main()
