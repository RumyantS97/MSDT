import json
import csv
import re


def write_to_json_file(path: str, data: dict) -> None:
    """
    writes a dict to json file
    """
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file)
    

def read_csv(path: str) -> list[list[str]]:
    """
    read csv file
    """
    data = []
    with open(path, "r", encoding="utf-16") as file:
        file_reader = csv.reader(file, delimiter=';')
        next(file_reader, None)
        for row in file_reader:
            data.append(row)
        return data
    

def validate_rows(data: list[list[str]], regular: dict) -> list[int]:
    """
    validate rows in a dataset against a set of regular expression patterns
    """
    invalid_rows = []
    for number, row in enumerate(data):
        for _, (field, key) in enumerate(zip(row, regular.keys())):
            pattern = regular[key]
            if not re.fullmatch(pattern, field):
                invalid_rows.append(number)
                break
    return invalid_rows
