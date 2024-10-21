import csv
import re
from checksum import calculate_checksum, serialize_result

patterns = {
    "email": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    "http_status_message": r'^\d{3} [A-Za-z ]+$',
    "snils": r'^\d{11}$',
    "passport": r'^\d{2} \d{2} \d{6}$',
    "ip_v4": r'^(25[0-5]|2[0-4]\d|1\d{2}|\d{1,2})(\.(25[0-5]|2[0-4]\d|1\d{2}|\d{1,2})){3}$',
    "longitude": r'^(-?(180(\.0{1,6})?|(\d{1,2}|1[0-7]\d)(\.\d{1,6})?))$',
    "hex_color": r'^#[0-9a-fA-F]{6}$',
    "isbn": r'^(?:\d-\d{5}-\d{3}-\d|\d{3}-\d-\d{5}-\d{3}-\d)$',
    "locale_code": r'^[a-z]{2}(-[a-z]{2})?$',
    "time": r'^(2[0-3]|[01]\d):[0-5]\d:[0-5]\d(\.\d{1,6})?$'
}


# Проверка валидности строки
def validate_row(row):
    for key, pattern in patterns.items():
        if not re.match(pattern, row[key]):
            return False, key  # Возвращаем имя поля, которое не прошло проверку
    return True, None


# Чтение и проверка CSV файла
def check_csv_file(filename):
    invalid_row_nums = []
    with open(filename, mode='r', encoding='utf-16') as file:
        reader = csv.DictReader(file, delimiter=';')
        for line_number, row in enumerate(reader, start=1):
            is_valid, invalid_field = validate_row(row)
            if not is_valid:
                invalid_row_nums.append(line_number-1)
        return invalid_row_nums


invalid_row_nums = check_csv_file('73.csv')
checksum = calculate_checksum(invalid_row_nums)

variant = 73
serialize_result(variant, checksum)
