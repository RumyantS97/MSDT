import pandas as pd
import re
from checksum import calculate_checksum, serialize_result

# Определяем регулярные выражения для валидации
validators = {
    "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    "telephone": r"^\+7-\(\d{3}\)-\d{3}-\d{2}-\d{2}$",
    "http_status_message": r"^\d{3} .+$",
    "height": r"^[0-2]\.\d{2}$",
    "snils": r"^\d{11}$",
    "inn": r"^\d{12}$",
    "passport": r"^\d{2} \d{2} \d{6}$",
    "identifier": r"^\d{2}-\d{2}/\d{2}$",
    "ip_v4": r"^((25[0-5]|2[0-4]\d|1\d{2}|\d{1,2})\.){3}(25[0-5]|2[0-4]\d|1\d{2}|\d{1,2})$",
    "occupation": r"^[A-Za-zА-Яа-яЁё\s-]+$",
    "longitude": r"^-?([1-8]?\d(\.\d+)?|90(\.0+)?)$",
    "latitude": r"^-?(1[0-7]\d(\.\d+)?|180(\.0+)?|[1-9]?\d(\.\d+)?)$",
    "hex_color": r"^#[0-9a-fA-F]{6}$",
    "blood_type": r"^(A|B|AB|O)[+-]$",
    "isbn": r"^\d{3}-\d{1,5}-\d{1,7}-\d{1,7}-\d{1}$",
    "issn": r"^\d{4}-\d{4}$",
    "locale_code": r"^[a-z]{2}-[a-z]{2}$",
    "uuid": r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    "time": r"^\d{2}:\d{2}:\d{2}\.\d{6}$",
    "date": r"^\d{4}-\d{2}-\d{2}$"
}


# Функция для проверки строки на валидность
def validate_row(row, validators):
    for column, regex in validators.items():
        value = str(row[column]) if column in row else ""
        if not re.match(regex, value):
            return False
    return True


# Загрузка данных
file_path = "33.csv"
data = pd.read_csv(file_path, encoding="utf-16-le", delimiter=";")

# Список строк с ошибками
invalid_rows = []

for idx, row in data.iterrows():
    if not validate_row(row, validators):
        invalid_rows.append(idx)

# Вычисление контрольной суммы
checksum = calculate_checksum(invalid_rows)

# Сериализация результата в result.json
serialize_result(33, checksum)
