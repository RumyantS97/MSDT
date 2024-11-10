import re
import csv
from checksum import calculate_checksum, serialize_result

regular_expressions = {
     'telephone':r'^\+7-\(\d{3}\)-\d{3}(?:-\d{2}){2}$',
     'height':r'^[1-2]\.\d{2}$',
     'snils':r'^[0-9]{11}$',
     'identifier':r'^\d{2}-\d{2}\/\d{2}$',
     'occupation':r'^[A-Za-zА-Яа-яёЁ\s-]+$',
     'longitude':r'^-?(180|(\d|\d{2}|1[0-7]\d)(\.\d+)?)$',
     'blood_type':r'^(A|B|AB|O)(\+|\u2212)$',
     'issn':r'^\d{4}-\d{4}$',
     'locale_code':r'^([a-z]{2}|[a-z]{2}-[a-z]{2})$',
     'date':r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$'
}

def check_row(row: dict):

    for key, value in regular_expressions.items():
        if not re.match(value, row[key]):
            return False
    return True

def process_file():
    row_number = []
    with open('92.csv', newline='', encoding='utf-16') as file:
        reader =csv.DictReader(file, delimiter=';')
        for number, row in enumerate(reader, start = 2):
            if not(check_row(row)):
                row_number.append(number - 2)
    return row_number

variant = 92
row_numbers = process_file()
print(len(row_numbers))
checksum= calculate_checksum(row_numbers)
serialize_result(variant, checksum)
