import re
import csv
import os
from checksum import calculate_checksum, serialize_result


regular_expressions = {
    'telephone': r'^\+7-\([0-9]{3}\)-\d{3}-\d{2}-\d{2}$',
    'height': r'^[1-2]\.\d{2}$',
    'snils': r'^[0-9]{11}$',
    'identifier': r'^\d{2}-\d{2}\/\d{2}$',
    'occupation': r'^[A-Za-zА-Яа-яёЁ\s-]+$',
    'longitude': r'^-?(180|(\d{1,2}|1[0-7]\d)(\.\d{1,})?)$',
    'blood_type': r'^(A|B|AB|O)(\+|\u2212)$',
    'issn': r'^[0-9]{4}-[0-9]{4}$',
    'locale_code': r'^([a-z]|[A-Z])+((-([a-z]|[A-Z])+)+)?$',
    'date': r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$'
}


def check_row(row):
    for key, expression in regular_expressions.items():
        if not re.match(expression, row[key]):
            print("error: " + key + "|" + row[key] + "|")
            return False
    return True


def check_file():
    with open('msdt-3/84.csv', newline='', encoding='utf-16') as file:
        reader = csv.DictReader(file, delimiter=';')
        index = 0
        invalid_rows = []
        for row in reader:
            if not check_row(row):
                #print(row)
                invalid_rows.append(index)
            index += 1
        return invalid_rows


variant = 84
#print(check_file())
#print(len(check_file()))
checksum = calculate_checksum(check_file())
serialize_result(variant, checksum)