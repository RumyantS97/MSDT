import re
import csv
from checksum import calculate_checksum, serialize_result

regular_expressions = {
    'telephone': r'^\+7-\(\d{3}\)-\d{3}-\d{2}-\d{2}$',
    'height': r'^[1-2]\.\d{2}$',
    'inn': r'^\d{12}$',
    'identifier': r'^\d{2}-\d{2}/\d{2}$',
    'occupation': r'^[A-Za-zА-Яа-яёЁ\s-]+$',
    'latitude': r'^(-?(90(\.0+)?|[1-8]?\d(\.\d+)?))$',
    'blood_type': r'^(A|B|AB|O)(\+|\u2212)$',
    'issn': r'^\d{4}-\d{4}$',
    'uuid': r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}'
            r'-[0-9a-fA-F]{12}$',
    'date': r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$'
}


def check_row(row):
    for key, expression in regular_expressions.items():
        if not re.match(expression, row[key]):
            return False
    return True


def check_file():
    with open('72.csv', newline='', encoding='utf-16') as file:
        reader = csv.DictReader(file, delimiter=';')
        index = 0
        invalid_rows = []
        for row in reader:
            if not check_row(row):
                invalid_rows.append(index)
            index += 1
        return invalid_rows


variant = 72
checksum = calculate_checksum(check_file())
serialize_result(variant, checksum)
