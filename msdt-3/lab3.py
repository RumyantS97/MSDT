import csv
import re
from checksum import calculate_checksum, serialize_result

patterns = {
    "telephone": r"^\+7-\(\d{3}\)-\d{3}-\d{2}-\d{2}$",
    "height": r"^[12]\.\d{2}$",
    "snils": r'^\d{11}$',
    "identifier": r"^\d{2}-\d{2}/\d{2}$",
    "occupation": r"^[A-Za-zА-Яа-яёЁ\s-]+$",
    "longitude": r'^(-?(180(\.0{1,6})?|(\d{1,2}|1[0-7]\d)(\.\d{1,6})?))$',
    "blood_type": r"^(A|B|AB|O)[\u2212\+]{1}$",
    "issn": r"^\d{4}-\d{4}$",
    "locale_code": r'^[a-z]{2}(-[a-z]{2})?$',
    "date": r"^(19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"
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


invalid_row_nums = check_csv_file('68.csv')
checksum = calculate_checksum(invalid_row_nums)
variant = 68
serialize_result(variant, checksum)
