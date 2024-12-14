import pandas as pd
import re
from checksum import calculate_checksum, serialize_result

# Определяем регулярные выражения для валидации
validators = {
    "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    "height": r"^\d{1}\.\d{2}$",
    "inn": r"\d{12}",
    "passport": r"^\d{2} \d{2} \d{6}$",
    "occupation": r"[а-яА-Яa-zA-Z\- ]+",
    "latitude": r"^-?(90(\.0+)?|((1[0-7]\d)|(\d{1,2}))(\.\d+)?)$",
    "hex_color": r"^#[0-9a-fA-F]{6}$",
    "issn": r"\d{4}-\d{4}",
    "uuid": r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}",
    "time": r"^([01]\d|2[0-3]):[0-5]\d:[0-5]\d\.\d+$",
}


def validate_row(row, validators):
    for column, regex in validators.items():
        value = str(row[column]) if column in row else ""
        if not re.match(regex, value):
            return False
    return True



file_name = "47.csv"
data = pd.read_csv(file_name, encoding="utf-16-le", delimiter=";")


invalid_rows = []

for idx, row in data.iterrows():
    if not validate_row(row, validators):
        invalid_rows.append(idx)


checksum = calculate_checksum(invalid_rows)


serialize_result(33, checksum)