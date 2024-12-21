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


def invalid_list(data: list[list[str]], patern: dict) -> list[int]:
    """
    Get invalide indexs
    """
    invalid_rows = []

    for row_number, row in enumerate(data):
        for col_index, (field, key) in enumerate(zip(row, patern.keys())):
            pattern = patern[key]
            if not re.fullmatch(pattern, field):
                invalid_rows.append(row_number)
                break 

    return invalid_rows
