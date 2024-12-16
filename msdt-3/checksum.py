import re
import json
import hashlib
import pandas as pd

def calculate_checksum(row_numbers):
    """
    Вычисляет md5 хеш от списка целочисленных значений.
    ВНИМАНИЕ: Первая строка с данными csv-файла имеет номер 0.
    """
    row_numbers.sort()
    return hashlib.md5(json.dumps(row_numbers).encode('utf-8')).hexdigest()

def serialize_result(variant: int, checksum: str) -> None:
    """
    Сериализация результата в result.json.
    :param variant: номер вашего варианта
    :param checksum: контрольная сумма
    """
    result = {"variant": variant, "checksum": checksum}
    with open("result.json", "w") as f:
        json.dump(result, f)

def validate_csv(file_path: str, variant: int):
    """
    Валидирует CSV-файл, используя регулярные выражения, и подсчитывает контрольную сумму.
    :param file_path: путь к CSV-файлу
    :param variant: номер вашего варианта
    """
    # Регулярные выражения для валидации данных
    regex_patterns = {
        'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        'http_status_message': r'^\d{3} [A-Za-z ]+$',
        'snils': r'^\d{11}$',
        'passport': r'^\d{2} \d{2} \d{6}$',
        'ip_v4': r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',
        'longitude': r'^-?\d+(\.\d+)?$',
        'hex_color': r'^#[0-9a-fA-F]{6}$',
        'isbn': r'^\d{1,5}-\d{1,7}-\d{1,7}-\d{1,7}(-\d{1,7})?$',
        'locale_code': r'^[a-z]{2}(-[a-zA-Z]{2,3})?$',
        'time': r'^\d{2}:\d{2}:\d{2}\.\d{6}$'
    }

    # Загружаем данные с правильной кодировкой
    data = pd.read_csv(file_path, encoding='utf-16', sep=';', low_memory=False)

    # Список для хранения номеров невалидных строк
    invalid_rows = set()

    # Проверяем каждую строку
    for index, row in data.iterrows():
        for column, pattern in regex_patterns.items():
            if not re.match(pattern, str(row[column])):
                invalid_rows.add(index)
                break  # Достаточно одного невалидного поля на строку

    # Считаем контрольную сумму
    invalid_row_numbers = sorted(invalid_rows)
    checksum = calculate_checksum(invalid_row_numbers)

    # Записываем результат
    serialize_result(variant, checksum)
    print(f"Контрольная сумма: {checksum}")

if __name__ == "__main__":
    # Путь к вашему CSV-файлу
    file_path = "65.csv"  # Замените на ваш путь
    variant = 65  # Ваш номер варианта
    validate_csv(file_path, variant)
