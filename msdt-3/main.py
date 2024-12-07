import pandas as pd
import re
from checksum import calculate_checksum, serialize_result

# Определяем регулярные выражения для валидации
validators = {
    "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    "http_status_message": r"^\d{3} .+$",
    "snils": r"^\d{11}$",
    "passport": r"^\d{2} \d{2} \d{6}$",
    "ip_v4": r"^((25[0-5]|2[0-4]\d|1\d{2}|\d{1,2})\.){3}(25[0-5]|2[0-4]\d|1\d{2}|\d{1,2})$",
    "longitude": r"^-?([1-8]?\d(\.\d+)?|90(\.0+)?)$",
    "hex_color": r"^#[0-9a-fA-F]{6}$",
    "isbn": r"^\d{3}-\d{1,5}-\d{1,7}-\d{1,7}-\d{1}$",
    "locale_code": r"^[a-z]{2}-[a-z]{2}$",
    "time": r"^\d{2}:\d{2}:\d{2}\.\d{6}$",
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
