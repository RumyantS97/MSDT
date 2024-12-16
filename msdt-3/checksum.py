import csv
import re
import json
import hashlib

# Регулярные выражения для валидации данных
PATTERNS = {
    'telephone'            : r"^\+7-\(\d{3}\)-\d{3}-\d{2}-\d{2}$",
    'http_status_message'  : r"^\d{3} .+$",
    'snils'                : r'^\d{11}$',
    'identifier'           : r"^\d+[-/]\d+[-/]\d+$",
    'ip_v4'                : r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){2}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
    'longitude'            : r'^-?(180(\.0+)?|((1[0-7][0-9])|([1-9]?[0-9]))(\.\d+)?)$',
    'blood_type'           : r'^(A|B|AB|O)[+\u2212]$',
    'isbn'                 : r'^\d+-\d+-\d+-\d+(?:-\d+)?$',
    'locale_code'          : r'^[a-z]{2}(?:-[a-z]{2})?$',
    'date'                 : r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$'
}

# Путь к CSV-файлу
csv_file_path = "34.csv"  # Укажите путь к вашему файлу
# Путь к JSON-файлу результата
result_json_path = "result.json"

# Список для хранения номеров невалидных строк
invalid_row_numbers = []

# Чтение CSV-файла и валидация данных
with open(csv_file_path, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file, delimiter=";")  # Предполагается, что разделитель — точка с запятой
    for row_number, row in enumerate(reader, start=1):  # Нумерация начинается с 1
        for field, pattern in PATTERNS.items():  # Проверяем каждую колонку строки
            value = row[field].strip()  # Убираем лишние пробелы
            if not re.match(pattern, value):  # Если значение не соответствует регулярному выражению
                invalid_row_numbers.append(row_number)  # Добавляем номер строки
                break  # Прерываем проверку остальных колонок строки


# Вычисление контрольной суммы (сумма номеров всех невалидных строк)
control_sum = sum(invalid_row_numbers)
# Хеширование контрольной суммы
hashed_checksum = hashlib.md5(json.dumps(control_sum).encode('utf-8')).hexdigest()

# Создаем JSON с результатами
result = {
    "variant": "34",
    "checksum": hashed_checksum
}

# Записываем результат в JSON
with open(result_json_path, "w", encoding="utf-8") as json_file:
    json.dump(result, json_file, indent=4)

