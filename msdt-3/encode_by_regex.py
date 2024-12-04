import pandas as pd
import re
from checksum import serialize_result, calculate_checksum

regex = {
    "telephone": r"^\+7-\(\d{3}\)-\d{3}-\d{2}-\d{2}$",
    "height": r"^([1-2]\.\d{2})$",
    "snils": r"^\d{11}$",
    "identifier": r"^\d{2}-\d{2}/\d{2}$",
    "occupation": r"^[a-zA-Zа-яА-Я]+([ -][a-zA-Zа-яА-Я]+)*$",
    "longitude": r"^-?(?:180(?:\.0{1,6})?|(?:[0-9]|[1-9][0-9]|"
                 r"1[0-7][0-9])(?:\.\d{1,6})?)$",
    "blood_type": r"^(A|B|AB|O)(\+|\u2212|-)$",
    "issn": r"^\d{4}-\d{4}$",
    "locale_code": r"^[a-z]{2}(-[a-z]{2})?$",
    "date": r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$",
}
def check_date_value(date_string):
    date_list = list(map(int, date_string.split('-')))
    year = date_list[0]
    month = date_list[1]
    day = date_list[2]

    months_days = {
        1: 31,
        2: 29 if (year % 4 == 0 and (year % 100 != 0
                                     or year % 400 == 0)) else 28,
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

    if day > months_days.get(month, 0):
        return False

    return True


def check_ip_value(ip_string):
    ip_list = list(map(int, ip_string.split('.')))
    for num in ip_list:
        if (num > 255):
            return False
    return True


df = pd.read_csv("28.csv", encoding="utf-16", delimiter=';')
invalidate_row_numbers = []
count = 0
cnt = 0

# Словарь для хранения количества некорректных значений для каждого поля
invalid_field_counts = {key: 0 for key in regex.keys()}

for row_index, row in df.iterrows():
    for column_name, value in row.items():
        pattern = regex.get(column_name)

        if pd.isna(value):
            # Если значение пустое или NaN
            if column_name == "date":
                cnt += 1
            invalidate_row_numbers.append(row_index)
            count += 1
            invalid_field_counts[column_name] += 1
            break

        if pattern:
            isValidate = re.fullmatch(pattern, value)

            # Дополнительная проверка для даты
            if isValidate and column_name == "date":
                if not check_date_value(value):
                    isValidate = False

            if not isValidate:
                if column_name == "date":
                    cnt += 1
                invalidate_row_numbers.append(row_index)
                count += 1
                invalid_field_counts[column_name] += 1
                break

# Сериализация результата
serialize_result(28, calculate_checksum(invalidate_row_numbers))

# Вывод количества некорректных значений для каждого поля (для отладки)
print("\nКоличество некорректных значений для каждого поля:")
for field, count in invalid_field_counts.items():
    print(f"{field}: {count}")
