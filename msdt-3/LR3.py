import csv
import re
from checksum import calculate_checksum, serialize_result

patterns = {
    'email': r'[A-Za-z0-9]+\.*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+$',
    'height': r'^[1-2]\.\d{2}$',
    'snils': r'^\d{11}$',
    'passport': r'^\d{2}\s\d{2}\s\d{6}$',
    'occupation': r'^[A-Za-zА-Яа-яёЁ\s-]+$',
    'longitude': r'^(-?(180(\.0{1,6})?|(1[0-7]\d|\d{1,2})(\.\d{1,6})?))$',
    'hex_color': r'^#[0-9a-fA-F]{6}$',
    'issn': r'^\d{4}-\d{4}$',
    'locale_code': r'^[a-z]{2}(-[a-z]{2}?)?$',
    'time': r'^(2[0-3]|[01]\d):([0-5]\d):([0-5]\d)(\.\d{1,6})?$'
}


def get_valid_row(row):
    # Определение валидных строк
    for str, pattern in patterns.items():
        if not re.match(pattern, row[str]):
            return False
    return True


def check_file():
    # Проверка файла на валидность строк
    with open('11.csv', newline='', encoding='utf-16') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        invalid_row_nums = []
        i = 1
        for row in reader:
            i += 1
            if not get_valid_row(row):
                invalid_row_nums.append(i-2)
        return invalid_row_nums


invalid_row_nums = check_file()
checksum = calculate_checksum(invalid_row_nums)

variant = 11
serialize_result(variant, checksum)

