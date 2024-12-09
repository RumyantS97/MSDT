import csv
import re

from checksum import serialize_result, calculate_checksum

# Определение регулярных выражений
regex_patterns = {
    'email': r'^[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]{2,}$',
    'height': r'^([1-2]\.\d{2})$',
    'inn': r'^\d{12}$',
    'passport': r'^\d{2} \d{2} \d{6}$',
    'occupation': r'^[a-zA-Zа-яА-Я]+([ -][a-zA-Zа-яА-Я]+)*$',
    'latitude': r'^-?\d{1,2}\.\d+$',
    'hex_color': r'^#[a-fA-F0-9]{6,8}$',
    'issn': r'^\d{4}-\d{4}$',
    'uuid': r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$',
    'time': r'^[0-2]\d:[0-5]\d:[0-5]\d(\.\d{1,6})?$'
}


# Проверка строки на соответствие шаблону
def check_row(row):
    for column_name, regex_pattern in regex_patterns.items():
        if not re.match(regex_pattern, str(row[column_name])):
            return False

    return True
# Обработка CSV-файл построчно и проверяет каждую строку на соответствие шаблонам
def procces_csv():
    incorrect_rows = []
    with open('55.csv', mode='r', encoding='utf-16', newline='') as file:
        reader = csv.DictReader(file, delimiter=';')
        for index, row in enumerate(reader):
            if not check_row(row):
                incorrect_rows.append(index)
    return incorrect_rows


rows = procces_csv()
print(calculate_checksum(rows))
serialize_result(55, calculate_checksum(rows))
