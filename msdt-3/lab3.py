import re
import csv

from checksum import calculate_checksum, serialize_result


PATTERNS = {
    'telephone': r'^\+7-\(\d{3}\)-\d{3}-\d{2}-\d{2}$',
    'height': r'^[1-2]\.\d{2}$',
    'snils': r'^\b\d{11}\b',
    'identifier': r'^\d{2}-\d{2}/\d{2}$',
    'occupation': r'^[A-Za-zА-Яа-яёЁ\s-]+$',
    'longitude': r'^(-?(180(\.0{1,6})?|(\d{1,2}|1[0-7]\d)(\.\d{1,6})?))$',
    'blood_type': r'^(A|B|AB|O)(\+|\u2212)$',
    'issn': r'^\d{4}-\d{4}$',
    'locale_code': r'^[a-z]{2}(-[a-z]{2})?$',
    'date': r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$'
}

def check_row(row: dict) -> bool:
    """
    Проверяет строку из файла csv на соответствие паттернам.
    """
    for key, pattern in PATTERNS.items():
        if not(re.match(pattern, row[key])):
            print(row[key])
            return False
    return True

def read_my_csv() -> list:
    """
    Метод для прохождения по ячейкам csv файла (кроме заголовков)
    и проверки каждой строчки на соответствие паттернам при помощи check_row.
    """
    row_numbers = []
    with open('76.csv', newline='', encoding='utf-16') as file:
        reader = csv.DictReader(file, delimiter=';')
        for number, row in enumerate(reader, start=2):
            if not(check_row(row)):
                row_numbers.append(number - 2)
    return row_numbers

variant = 76
row_numbers = read_my_csv()
print(len(row_numbers))
checksum = calculate_checksum(row_numbers)
serialize_result(variant, checksum)
