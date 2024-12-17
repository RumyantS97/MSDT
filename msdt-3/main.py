import re
import csv
from checksum import calculate_checksum, serialize_result

# Обновленные регулярные выражения для проверки данных
regular_expressions = {
    # Номер телефона: формат +7-(XXX)-XXX-XX-XX
    'telephone': r'^\+7-\(\d{3}\)-\d{3}-\d{2}-\d{2}$',

    # HTTP статус сообщения: трехзначный код и текст
    'http_status_message': r'^\d{3} [A-Za-z0-9 ]+$',

    # СНИЛС: 11 цифр подряд
    'snils': r'^\d{11}$',

    # Идентификатор: цифры разделены спецсимволами (пример: 62-71/26)
    'identifier': r'^\d{2}-\d{2}/\d{2}$',

    # IPv4-адрес: стандартный формат IPv4
    'ip_v4': r'^(?:\d{1,3}\.){3}\d{1,3}$',

    # Долгота: числовое значение с плавающей точкой (пример: 92.264847, -63.65076)
    'longitude': r'^-?(180(\.0+)?|1[0-7]\d(\.\d+)?|\d{1,2}(\.\d+)?)$',

    # Группа крови с резус-фактором (пример: AB+, O−)
    'blood_type': r'^(A|B|AB|O)[+-−]$',

    # ISBN: 13 цифр с разделителями (пример: 018-1-50114-053-6)
    'isbn': r'^\d{3}-\d-\d{5}-\d{3}-\d$',

    # Локальный код языка в формате MS-LCID (пример: es-uy,xh)
    'locale_code': r'^[a-z]{2}(-[a-z]{2})?(,[a-z]{2})*$',

    # Дата в формате ГГГГ-ММ-ДД
    'date': r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$'
}


def check_row(row):
    """
    Проверка строки на соответствие всем правилам.
    """
    for key, expression in regular_expressions.items():
        if key in row and not re.match(expression, row[key]):
            print(f"Error in field {key}: {row[key]}")
            return False
    return True


def check_file():
    """
    Проверка всех строк файла и возврат списка некорректных строк.
    """
    invalid_rows = []
    with open('74.csv', newline='', encoding='utf-16') as file:
        reader = csv.DictReader(file, delimiter=';')
        for index, row in enumerate(reader):
            if not check_row(row):
                invalid_rows.append(index)
        print(f"Invalid rows count: {len(invalid_rows)}")
    return invalid_rows


variant = 74
invalid_rows = check_file()
checksum = calculate_checksum(invalid_rows)
serialize_result(variant, checksum)
