import csv
import re
import json
import hashlib
from typing import List


PATTERNS = {
    'email': r'^\S+@\S+\.\S+$',
    'height': r'^[1-2]\.\d{2}$',
    'inn': r'^\d{12}$',
    'passport': r'^\d{2} \d{2} \d{6}$',
    'occupation': r'^[A-Za-zА-Яа-я\s\-]+$',
    'latitude': r'^-?\d{1,2}\.\d+$',
    'hex_color': r'^#[0-9a-fA-F]{6}$',
    'issn': r'^\d{4}-\d{4}$',
    'uuid': r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$',
    'time': r'^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d(?:\.\d{1,6})?$'
}

def is_valid(row: dict) -> bool:
    """
    Проверяет, соответствует ли строка всем заданным паттернам.
    :param row: строка из файла, представлена как словарь
    :return: True, если все поля соответствуют своим шаблонам; иначе False
    """
    for field, pattern in PATTERNS.items():
        if not re.match(pattern, row[field]):
            return False
    return True


# Инициализация списков для хранения невалидных строк и их номеров
invalid_rows = []
invalid_row_numbers = []

# Открываем и проверяем файл
with open('71.csv', newline='', encoding='utf-16') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row_number, row in enumerate(reader, start=2):  # Начинаем с 2, чтобы учитывать заголовок
        if not is_valid(row):
            invalid_rows.append(row)
            invalid_row_numbers.append(row_number - 2)


def calculate_checksum(row_numbers: List[int]) -> str:
    """
    Вычисляет md5 хеш от списка целочисленных значений.

    :param row_numbers: список номеров строк
    :return: md5 хеш строки
    """
    row_numbers.sort()
    return hashlib.md5(json.dumps(row_numbers).encode('utf-8')).hexdigest()


def serialize_result(variant: int, checksum: str) -> None:
    """
    Метод для сериализации результатов лабораторной работы.
    Записывает номер варианта и контрольную сумму в файл result.json.

    :param variant: номер варианта
    :param checksum: контрольная сумма, вычисленная через calculate_checksum()
    """
    result = {
        "variant": variant,
        "checksum": checksum
    }

    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)


# Основная часть программы
VARIANT_NUMBER = 71  # Укажите ваш номер варианта
checksum = calculate_checksum(invalid_row_numbers)
print(checksum)
serialize_result(VARIANT_NUMBER, checksum)