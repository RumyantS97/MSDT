import csv
import json
import hashlib
import re
from typing import List
from io import StringIO
from charset_normalizer import detect

# Регулярные выражения для проверки данных
PATTERNS = {
    "email"              : r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$",
    "http_status_message": r"^\d{3} [\w\s]+$",
    "inn"                : r"^\d{12}$",
    "passport"           : r"^\d{2} \d{2} \d{6}$",
    "ip_v4"              : r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",
    "latitude"           : r"^-?\d+(\.\d+)?$",
    "hex_color"          : r"^#[0-9a-fA-F]{6}$",
    "isbn"               : r"^(?:\d{3}-)?\d-\d{5}-\d{3}-\d$",
    "uuid"               : r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$",
    "time"               : r"^(2[0-3]|[01]?\d):[0-5]?\d:[0-5]?\d(\.\d+)?$"
}

def calculate_checksum(row_numbers: List[int]) -> str:
    """
    Вычисляет md5 хеш от списка целочисленных значений.
    :param row_numbers: список целочисленных номеров строк csv-файла, на которых были найдены ошибки валидации
    :return: md5 хеш для проверки через github action
    """
    row_numbers.sort()
    return hashlib.md5(json.dumps(row_numbers).encode('utf-8')).hexdigest()

def serialize_result(variant: int, checksum: str) -> None:
    """
    Сериализует результаты в JSON-файл result.json.
    :param variant: номер варианта
    :param checksum: контрольная сумма
    """
    result = {
        "variant": variant,
        "checksum": checksum
    }

    with open("result.json", "w", encoding="utf-8") as result_file:
        json.dump(result, result_file, ensure_ascii=False, indent=4)

def validate_field(field_name: str, value: str) -> bool:
    """
    Проверяет значение поля на валидность по регулярному выражению.
    :param field_name: Название поля
    :param value: Значение поля
    :return: True, если значение валидно, иначе False
    """
    pattern = PATTERNS.get(field_name)
    if pattern:
        return re.match(pattern, value.strip()) is not None
    return False

def validate_csv(file_path: str) -> List[int]:
    """
    Проверяет CSV-файл на наличие ошибок.
    :param file_path: Путь к файлу
    :return: Список номеров строк с ошибками
    """
    error_rows = []

    # Определяем кодировку файла
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        detected = detect(raw_data)
        encoding = detected['encoding']
        if not encoding:
            raise ValueError("Не удалось определить кодировку файла.")

        # Декодируем содержимое файла
        content = raw_data.decode(encoding)

    # Убираем BOM, если он присутствует
    if content[:1] == '\ufeff':
        content = content[1:]

    # Работаем с декодированным содержимым
    csvfile = StringIO(content)
    reader = csv.DictReader(csvfile, delimiter=';')

    for row_num, row in enumerate(reader):
        adjusted_row_num = row_num  # Учитываем, что первая строка с данными имеет номер 0
        for field, value in row.items():
            # Убираем кавычки вокруг ключей (если они есть) и проверяем поля
            field_name = field.strip('"')
            if field_name in PATTERNS and not validate_field(field_name, value):
                error_rows.append(adjusted_row_num)
                break
    return error_rows

def main():
    csv_file_path = "37.csv"
    variant = 37

    try:
        # Валидация и подсчет контрольной суммы
        error_rows = validate_csv(csv_file_path)
        checksum = calculate_checksum(error_rows)

        # Сериализация результатов
        serialize_result(variant, checksum)
    except ValueError as e:
        print(f"Ошибка: {e}")
    except FileNotFoundError:
        print(f"Ошибка: Файл {csv_file_path} не найден.")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")

if __name__ == "__main__":
    main()
