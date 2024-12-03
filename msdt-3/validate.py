import re
import pandas as pd
import csv
import json
import hashlib
from checksum import * 


regex_patterns = {
    "telephone":          r"^\+7-\(\d{3}\)-\d{3}-\d{2}-\d{2}$", # Телефон в формате +7-(XXX)-XXX-XX-XX
    "http_status_message": r"^\d{3}\s.+", # HTTP статус, например, 200 OK
    "inn":                r"^\d{12}$", # ИНН - 12 цифр
    "identifier":         r"^\d{2}-\d{2}/\d{2}$", # Идентификатор формата XX-YY/ZZ
    "ip_v4":              r"^\d{1,3}(\.\d{1,3}){3}$", # IPv4 адрес
    "latitude":           r"^-?\d{1,2}\.\d+$", # Широта (десятичное число)
    "blood_type":         r"^(A|B|AB|O)[+-]$", # Группа крови A+/-, B+/-, O+/-, AB+/-
    "isbn":               r"^\d{3}-\d{1,5}-\d{1,7}-\d{1,7}-\d{1}$", # ISBN в формате XXX-X-XXXX-XXXX-X
    "uuid":               r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", # UUID
    "date":               r"^\d{4}-\d{2}-\d{2}$" # Дата в формате YYYY-MM-DD
}



file_path = r'C:\Users\dasha\OneDrive\Рабочий стол\гитхаб\MSDT\msdt-3\86.csv'

# Определяем кодировку файла автоматически
import chardet
with open(file_path, 'rb') as f:
    rawdata = f.read(2000)
    result = chardet.detect(rawdata)
    encoding = result['encoding']

# Определяем разделитель файла автоматически
with open(file_path, 'r', encoding=encoding) as f:
    sample = f.read(2000)
    dialect = csv.Sniffer().sniff(sample)


data = pd.read_csv(file_path, encoding=encoding, delimiter=dialect.delimiter)

# Функция для валидации строки
def validate_row(row):
    invalid_columns = []
    for col, pattern in regex_patterns.items():
        if not re.match(pattern, str(row[col])):
            invalid_columns.append(col)
    return invalid_columns


invalid_rows = []


for index, row in data.iterrows():
    if validate_row(row):
        invalid_rows.append(index - 1)  # Сдвигаем на -1, чтобы 2-я строка стала 0-й

# Удаляем отрицательные индексы
invalid_rows = [i for i in invalid_rows if i >= 0]

# Подсчитываем контрольную сумму
checksum = calculate_checksum(invalid_rows)

variant_number = 86  
checksum_value = calculate_checksum(invalid_rows)  

serialize_result(variant_number, checksum_value)  


print(f"Контрольная сумма ({checksum}) сохранена в result.json")
