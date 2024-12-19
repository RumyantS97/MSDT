import pandas as pd
import re
from checksum import calculate_checksum, serialize_result

# Обновлённые регулярные выражения для нового формата
validators = {
    "telephone": r"^\+7-\(\d{3}\)-\d{3}-\d{2}-\d{2}$",
    "height": r"^\"?\d{1}\.\d{2}\"?$",
    "inn": r"^\d{12}$",
    "identifier": r"^\d{2}-\d{2}/\d{2}$",
    "occupation": r"^[а-яА-Яa-zA-Z\- ]+$",
    "latitude": r"^-?(90(\.0+)?|([1-8]?\d(\.\d+)?))$",
    "blood_type": r"^(A|B|AB|O)[+-]$",
    "issn": r"^\d{4}-\d{4}$",
    "uuid": r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$",
    "date": r"^\d{4}-\d{2}-\d{2}$",
}


def validate_row(row, validators):
    """Функция валидации строки по регулярным выражениям."""
    for column, regex in validators.items():
        value = str(row[column]) if column in row and pd.notna(row[column]) else ""
        if not re.match(regex, value):
            return False
    return True


file_name = "56.csv"
data = pd.read_csv(file_name, encoding="utf-16-le", delimiter=";", quotechar='"')
invalid_rows = []
# Проверяем строки
for idx, row in data.iterrows():
    if not validate_row(row, validators):
        invalid_rows.append(idx)
# Считаем чек-сумму и сериализуем результат
checksum = calculate_checksum(invalid_rows)
serialize_result(56, checksum)