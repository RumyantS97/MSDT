import csv
import re
import json
import hashlib
from typing import List

# Шаблоны регулярных выражений для проверки значений
validation_rules = {
    'email'     : r'^[\w\.\+-]+@[\w-]+\.[a-z]{2,}$',
    'height'    : r'^[1-2]\.[0-9]{2}$',
    'inn'       : r'^\d{12}$',
    'passport'  : r'^\d{2}\s\d{2}\s\d{6}$',
    'occupation': r'^[A-Za-zА-Яа-я\s\-]+$',
    'latitude'  : r'^-?\d{1,2}\.\d+$',
    'hex_color' : r'^#[0-9A-Fa-f]{6}$',
    'issn'      : r'^\d{4}-\d{4}$',
    'uuid'      : r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$',
    'time'      : r'^\d{2}:\d{2}:\d{2}\.\d{6}$'
}

def validate_row(data_row: dict) -> bool:
    """
    Проверяет корректность строки на основе заданных шаблонов.
    :param data_row: Словарь с данными строки.
    :return: True, если данные строки соответствуют шаблонам, иначе False.
    """
    for column_name, regex_pattern in validation_rules.items():
        if not re.match(regex_pattern, data_row[column_name]):
            return False
    return True

# Списки для хранения некорректных данных
invalid_records = []  # Некорректные строки
invalid_record_indices = []  # Индексы некорректных строк

# Загружаем файл и анализируем содержимое
row_index = 1
with open(r'79.csv', newline='', encoding='utf-16') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=';')
    for row in csv_reader:
        row_index += 1
        if not validate_row(row):
            invalid_records.append(row)
            invalid_record_indices.append(row_index - 2)

# Суммируем индексы некорректных строк
total_invalid_index_sum = sum(invalid_record_indices)
print(f"Сумма индексов некорректных строк: {total_invalid_index_sum}")

def compute_checksum(numbers: List[int]) -> str:
    """
    Генерирует MD5-хеш для списка чисел.
    :param numbers: Список целых чисел.
    :return: Хеш в формате строки.
    """
    numbers.sort()
    return hashlib.md5(json.dumps(numbers).encode('utf-8')).hexdigest()

def save_results(variant: int, checksum: str) -> None:
    """
    Записывает итоговые результаты в файл JSON.
    :param variant: Номер варианта.
    :param checksum: Контрольная сумма.
    """
    result_data = {
        "variant": variant,
        "checksum": checksum
    }
    with open('result.json', 'w', encoding='utf-8') as result_file:
        json.dump(result_data, result_file, ensure_ascii=False, indent=4)

# Указываем номер варианта
variant_id = 79

# Генерация контрольной суммы
checksum_value = compute_checksum(invalid_record_indices)
print(f"Контрольная сумма: {checksum_value}")

# Сохраняем данные
save_results(variant_id, checksum_value)