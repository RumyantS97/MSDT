import csv
import re
from checksum import calculate_checksum, serialize_result

# Регулярные выражения для валидации
regex_patterns = {
    'email'      :  r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
    'height'     :  r'^[0-9]{1,2}(\.[0-9]{1,2})?$',
    'inn'        :  r'^\d{10,12}$',
    'passport'   :  r'^\d{2} \d{2} \d{6}$',
    'occupation' :  r'^[A-Za-zА-Яа-яЁё\s]+$',
    'latitude'   :  r'^-?([1-8]?[0-9]|90)\.[0-9]+$',
    'hex_color'  :  r'^#[0-9a-fA-F]{6}$',
    'issn'       :  r'^\d{4}-\d{4}$',
    'uuid'       :  r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$',
    'time'       :  r'^\d{2}:\d{2}:\d{2}\.\d{6}$'
}

def validate_row(row):
    invalid_indexes = []
    # Проверка каждого столбца по регулярному выражению
    for i, (field, value) in enumerate(row.items()):
        pattern = regex_patterns.get(field)
        if pattern and not re.match(pattern, value):
            invalid_indexes.append(i)
    return invalid_indexes

# Чтение и валидация CSV файла
def validate_csv(file_path):
    invalid_rows = []
    with open(file_path, newline='', encoding='utf-16-le') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row_number, row in enumerate(reader, start=1):
            invalid_indexes = validate_row(row)
            if invalid_indexes:
                invalid_rows.append(row_number)
    return invalid_rows

file_path = "39.csv"
invalid_rows = validate_csv(file_path)

checksum = calculate_checksum(invalid_rows)
serialize_result(39, checksum)
print(checksum)