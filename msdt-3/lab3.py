import re
import pandas as pd
from typing import List
import hashlib
import json  # Модуль для вычисления контрольной суммы


def calculate_checksum(row_numbers: List[int]) -> str:
    """
    Вычисляет md5 хеш от списка целочисленных значений.

    ВНИМАНИЕ, ВАЖНО! Чтобы сумма получилась корректной, считать, что первая строка с данными csv-файла имеет номер 0
    Другими словами: В исходном csv 1я строка - заголовки столбцов, 2я и остальные - данные.
    Соответственно, считаем что у 2 строки файла номер 0, у 3й - номер 1 и так далее.

    :param row_numbers: список целочисленных номеров строк csv-файла, на которых были найдены ошибки валидации
    :return: md5 хеш для проверки через github action
    """
    row_numbers.sort()
    return hashlib.md5(json.dumps(row_numbers).encode('utf-8')).hexdigest()


def validate_telephone(telephone):
    pattern = r'^\+7-\(\d{3}\)-\d{3}-\d{2}-\d{2}$'
    return re.match(pattern, telephone) is not None


def validate_height(height):
    pattern = r'^(?:[1-2]?\d(\.\d{1,2})?|3(\.00)?)$'
    if re.match(pattern, str(height)):
        height_value = float(height)
        return 0.5 <= height_value <= 3.00
    return False


def validate_snils(snils):
    pattern = r'^\d{11}$'
    return re.match(pattern, snils) is not None


def validate_identifier(identifier):
    pattern = r'^\d{2}-\d{2}\/\d{2}$'
    return re.match(pattern, identifier) is not None


def validate_occupation(occupation):
    pattern = r'^[A-Za-zА-Яа-яёЁ\- ]+$'
    return re.match(pattern, occupation) is not None


def validate_longitude(longitude):
    pattern = r'^-?([1-8]?\d(\.\d+)?|90(\.0+)?)$'
    return re.match(pattern, longitude) is not None


def validate_blood_type(blood_type):
    pattern = r'^(A|B|AB|O)[\+\−]$'
    return re.match(pattern, blood_type) is not None


def validate_issn(issn):
    pattern = r'^\d{4}-\d{4}$'
    return re.match(pattern, issn) is not None


def validate_locale_code(uuid):
    pattern = r'^(?:[a-z]{2})(?:-[A-Z]{2})?$'
    return re.match(pattern, uuid) is not None


def validate_date(date):
    pattern = r'^\d{4}-(([0]\d)|([1][0-2]))-(([0-2]\d)|([3][0-1]))$'
    return re.match(pattern, date) is not None


def validate_data(data):
    validation_results = {
        'telephone': validate_telephone(data['telephone']),
        'height': validate_height(data['height']),
        'snils': validate_snils(data['snils']),
        'identifier': validate_identifier(data['identifier']),
        'occupation': validate_occupation(data['occupation']),
        'longitude': validate_longitude(data['longitude']),
        'blood_type': validate_blood_type(data['blood_type']),
        'issn': validate_issn(data['issn']),
        'locale_code': validate_locale_code(data['locale_code']),
        'date': validate_date(data['date']),
    }
    return validation_results


def serialize_result(variant, checksum):
    result = {
        'variant': variant,
        'checksum': checksum
    }
    with open('result.json', 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)


def read_and_validate_csv(file_path, variant_number):
    df = pd.read_csv(file_path, sep=";", encoding="utf-16")
    validation_results = []
    error_rows = []

    for index, row in df.iterrows():
        data = {
            'telephone': row.get('telephone'),
            'height': row.get('height'),
            'snils': row.get('snils'),
            'identifier': row.get('identifier'),
            'occupation': row.get('occupation'),
            'longitude': row.get('longitude'),
            'blood_type': row.get('blood_type'),
            'issn': row.get('issn'),
            'locale_code': row.get('locale_code'),
            'date': row.get('date'),
        }

        result = validate_data(data)
        validation_results.append(result)

        if any(not valid for valid in result.values()):
            error_rows.append(index)

    checksum = calculate_checksum(error_rows)
    serialize_result(variant_number, checksum)

    return validation_results, error_rows


if __name__ == "__main__":
    file_path = '12.csv'  # Укажите путь к вашему файлу CSV
    variant_number = 12

    validation_results, error_rows = read_and_validate_csv(file_path, variant_number)
