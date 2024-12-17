import csv
import re

from checksum import serialize_result, calculate_checksum

# Определение регулярных выражений
regex_patterns = {
    'email': r'^[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]{2,}$',
    'http_status_message': r'^\d{3} [A-Za-z ]+$',
    'snils': r'\d{11}$',
    'passport': r'^\d{2} \d{2} \d{6}$',
    'ip_v4': r'^((25[0-5]|(2[0-4]\d|1\d{2}|[1-9]?\d))\.){3}(25[0-5]|(2[0-4]\d|1\d{2}|[1-9]?\d))$',
    'longitude': r'^-?(180(\.0+)?|((1[0-7]\d)|(\d{1,2}))(\.\d+)?)$',
    'hex_color': r'^#[a-fA-F0-9]{6,8}$',
    'isbn': r'^(\d+-){3,5}\d+$',
    'locale_code': r'^[a-z]{2}-[a-z]{2}$',
    'time': r'^[0-2]\d:[0-5]\d:[0-5]\d(\.\d{1,6})?$'
}


# Проверка строки на соответствие всем шаблонам регулярных выражений
def validate_row(row):
    for column_name, pattern in regex_patterns.items():
        if not re.match(pattern, str(row[column_name])):
            return False
    return True


# Обработка CSV-файла и проверка каждой строки на соответствие шаблонам
def process_csv_file():
    invalid_rows_indices = []
    with open('65.csv', mode='r', encoding='utf-16', newline='') as file:
        reader = csv.DictReader(file, delimiter=';')
        for index, row in enumerate(reader):
            if not validate_row(row):
                invalid_rows_indices.append(index)
    return invalid_rows_indices


rows = process_csv_file()


serialize_result(65, calculate_checksum(rows))
