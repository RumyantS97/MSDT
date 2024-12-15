import csv
import re
import json
from typing import List, Dict
from checksum2 import calculate_checksum

# Регулярные выражения для валидации данных
PATTERNS = {
    'telephone': r"^\+7-\(\d{3}\)-\d{3}-\d{2}-\d{2}$",
    'http_status_message': r"^\d{3} .+$",
    'snils': r'^\d{11}$',
    'identifier': r"^\d+[-/]\d+[-/]\d+$",
    'ip_v4': r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){2}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
    'longitude': r'^-?(180(\.0+)?|((1[0-7][0-9])|([1-9]?[0-9]))(\.\d+)?)$',
    'blood_type': r'^(A|B|AB|O)[+\u2212]$',
    'isbn': '^\\d+-\\d+-\\d+-\\d+(?:-\\d+)?$',
    'locale_code': r'^[a-z]{2}(?:-[a-z]{2})?$',
    'date': r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$',
}

def is_valid(row: Dict[str, str]) -> bool:
    """
    Проверяет, соответствует ли строка всем заданным паттернам.

    :param row: строка из файла, представлена как словарь
    :return: True, если все поля соответствуют своим шаблонам; иначе False
    """
    for field, pattern in PATTERNS.items():
        if field in row and not re.match(pattern, row[field]):
            return False
    return True

def validate_csv(variant: int) -> List[int]:
    """
    Основная функция для проверки валидности данных в CSV файле.

    :param variant: номер варианта для имени файла
    :return: список номеров некорректных строк
    """
    invalid_row_numbers = []

    try:
        with open(f'{variant}.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row_number, row in enumerate(reader, start=2):
                if not is_valid(row):
                    invalid_row_numbers.append(row_number)

        print(f"Количество невалидных строк: {len(invalid_row_numbers)}")

    except FileNotFoundError:
        print(f"Файл {variant}.csv не найден.")
        return []

    except Exception as e:
        print(f"Произошла ошибка при обработке файла: {e}")
        return []

    return invalid_row_numbers

VARIANT_NUMBER = 34

def serialize_result(variant: int, checksum: str) -> None:
    """
    Сериализует результат проверки в JSON файл.

    :param variant: номер вашего варианта
    :param checksum: контрольная сумма, вычисленная через calculate_checksum()
    """
    result = {
        "variant": variant,
        "checksum": checksum
    }

    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # Получаем номера некорректных строк из validate_csv
    invalid_row_numbers = validate_csv(VARIANT_NUMBER)

    # Проверяем, есть ли некорректные строки перед вычислением контрольной суммы
    if invalid_row_numbers:
        checksum = calculate_checksum(invalid_row_numbers)
        serialize_result(VARIANT_NUMBER, checksum)
