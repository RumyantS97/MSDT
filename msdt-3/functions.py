import json
import csv
import re


def read_csv(path: str) -> list[list[str]]:
    """
    Reading CSV.
    """
    file_data = []
    with open(path, "r", encoding="utf-16") as file:
        file_reader = csv.reader(file, delimiter=';')
        next(file_reader, None)
        for row in file_reader:
            file_data.append(row)
        return file_data


def write_json(path: str, file_content: dict) -> None:
    """
    Write a data to a JSON file.
    """
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(file_content, file)


def check_validation(data: list, file_patterns: dict) -> bool:
    """
    Checking file validation by using patterns.
    """
    for key, value in zip(file_patterns.keys(), data):
        if not re.match(file_patterns[key], value):
            return False
    return True


def invalid_list(file_data: list, patterns: dict) -> list[int]:
    """
    Getting invalidated indexs.
    """
    invalid_list = []
    for i, row in enumerate(file_data):
        if not check_validation(row, patterns):
            invalid_list.append(i)
    return invalid_list
