import json
import hashlib
import re
from typing import Dict, List
import csv

validation_patterns: Dict[str, str] = {
    'email'        : r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'height'       : r'^[0-2]\.\d{2}$',
    'snils'        : r'^\d{11}$',
    'passport'     : r'^\d{2} \d{2} \d{6}$',
    'occupation'   : r'[a-zA-Zа-яА-ЯёЁ -]+',
    'longitude'    : r'^\-?(180|1[0-7][0-9]|\d{1,2})\.\d+$',
    'hex_color'    : r'^#[A-Fa-f0-9]{6}$',
    'issn'         : r'^\d{4}-\d{4}$',
    'locale_code'  : r'^[a-zA-Z]+(-[a-zA-Z]+)*$',
    'time'         : r'^\d{2}:\d{2}:\d{2}\.\d{6}$'
}


def check_row_patterns(row: List[str], row_index: int) -> bool:
    """
    Проверяет строку на соответствие паттернам.

    :param row: Список значений строки.
    :param row_index: Индекс строки в CSV файле.
    :return: True если найдена ошибка, False в противном случае.
    """
    for i, value in enumerate(row):
        field_name = list(validation_patterns.keys())[i]
        if not re.match(validation_patterns[field_name], value):
            print(f"Ошибка в строке {row_index + 2}, поле '{field_name}': "
                  f"значение '{value}' не соответствует шаблону.")
            return True
    return False


def process_csv(file_path: str) -> List[int]:
    """
    Обрабатывает CSV файл и возвращает индексы строк с ошибками.

    :param file_path: Путь к CSV файлу.
    :return: Список индексов строк с ошибками.
    """
    invalid_rows: List[int] = []

    try:
        with open(file_path, newline='', encoding='utf-16') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            next(reader)

            for row_index, row in enumerate(reader):
                if check_row_patterns(row, row_index):
                    invalid_rows.append(row_index)

    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")

    return invalid_rows


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
    Сохраняет результаты в JSON файл.

    :param variant: Номер вашего варианта.
    :param checksum: Контрольная сумма, вычисленная через calculate_checksum().
    """

    result_data = {
        "variant": variant,
        "checksum": checksum
    }

    try:
        # Проверяем существование файла и загружаем данные
        with open('result.json', 'r', encoding='utf-8') as json_file:
            existing_data = json.load(json_file)
            existing_data['checksum'] = checksum  # Обновляем контрольную сумму
            existing_data['variant'] = variant  # Обновляем номер варианта
            result_data.update(existing_data)

        # Сохраняем обновленные данные обратно в файл
        with open('result.json', 'w', encoding='utf-8') as json_file:
            json.dump(result_data, json_file, ensure_ascii=False, indent=4)

    except FileNotFoundError:
        # Если файл не существует, создаем новый с контрольной суммой и номером варианта
        with open('result.json', 'w', encoding='utf-8') as json_file:
            json.dump(result_data, json_file, ensure_ascii=False, indent=4)

    except OSError as er:
        raise OSError(f"Ошибка при сериализации результата: {er}")


def main():
    file_path = '51.csv'
    variant_number = 51

    invalid_row_indices = process_csv(file_path)

    if invalid_row_indices:
        checksum = calculate_checksum(invalid_row_indices)
        serialize_result(variant_number, checksum)
        print(f'Найдено {len(invalid_row_indices)} ошибок валидации. Контрольная сумма: {checksum}')
    else:
        print('Ошибок валидации не найдено.')


if __name__ == "__main__":
    main()

