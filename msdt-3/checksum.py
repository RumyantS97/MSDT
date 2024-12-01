import json
import hashlib
from typing import List
import pandas as pd
import re

patterns = {
    "telephone": r"^\+7-\(\d{3}\)-\d{3}-\d{2}-\d{2}$",
    "http_status_message": r"^\d{3} [A-Za-z ]+$",
    "inn": r"^\d{12}$",
    "identifier": r"^\d{2}-\d{2}/\d{2}$",
    "ip_v4": r"^(?:\d{1,3}\.){3}\d{1,3}$",
    "latitude": r"^-?(?:90(?:\.0{1,6})?|(?:[0-9]|[1-8][0-9])(?:\.\d{1,6})?)$",
    "blood_type": r"^(A|B|AB|O)(\+|\u2212|-)$",
    "isbn": r"^(?:\d{3}-)?\d-\d{5}-\d{3}-\d$",
    "uuid": r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    "date": r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$",
}

months_days = {
    1: 31,
    2: 29,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}

def calculate_checksum(row_numbers: List[int]) -> str:
    row_numbers.sort()
    return hashlib.md5(json.dumps(row_numbers).encode('utf-8')).hexdigest()


def serialize_result(variant: int, checksum: str) -> None:
    result = {
        "variant": str(variant),
        "checksum": checksum
    }

    with open("result.json", "w", encoding="utf-8") as file:
        json.dump(result, file, indent=2, ensure_ascii=False)


def check_date_value(date_string):
    date_list = list(map(int, date_string.split('-')))
    year = date_list[0]
    month = date_list[1]
    day = date_list[2]

    if (year < 1000
        or month > 12
        or day > months_days[month]
        or (day == 29 and month == 2 and year % 4 != 0)):

        return False

    return True


def check_ip_value(ip_string):
    ip_list = list(map(int, ip_string.split('.')))
    for num in ip_list:
        if (num > 255):
            return False
    return True


def check_latitude_value(latitude_string):
    latitude_value = float(latitude_string)
    if not (90.0 <= latitude_value <= 180.0):
        return False
    return True

# main
df = pd.read_csv("6.csv", encoding="utf-16", delimiter=';')
invalidate_row_numbers = []

for row_index, row in df.iterrows():
    for column_name, value in row.items():
        pattern = patterns[column_name]

        isValidate = re.fullmatch(pattern, value)

        if isValidate:
            if ((column_name == "date" and not check_date_value(value))
                or (column_name == "ip_v4" and not check_ip_value(value))
                or (column_name == "latitude" and
                    not check_latitude_value(value))):

                isValidate == False

        if not isValidate:
            invalidate_row_numbers.append(row_index)
            break

    serialize_result(6, calculate_checksum(invalidate_row_numbers))