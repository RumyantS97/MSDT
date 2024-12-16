import json
import csv
import re

from typing import Dict, List
from typing import Optional

from checksum import  calculate_checksum, serialize_result
from config import PATTERNS, PATH_TO_CSV, VARIANT


def get_json(path_name: str) -> Optional[Dict]:
    '''
    The function is for reading .json file and returns dictionary

    Args:
            path_name: path to .json file

    Returns:
            data: dictionary of regular expressions
    '''
    try:
        with open(path_name, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"The file was not found.")
    except Exception as e:
        print(f"An error occured while reading JSON the file: {str(e)}.")


def get_csv(path_name: str) -> Optional[List]:
    '''
    The function is for reading .csv file and returns list 
    of strings without a header string

    Args:
            path_name: path to .csv file

    Returns:
            data: a list of lists that contains lines from the file 
                  (without the header line)

    '''
    data = []
    try:
        with open(path_name, 'r', encoding='utf-16') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                data.append(row)
            data.pop(0)
        return data
    except FileNotFoundError:
        print(f"The file was not found.")
    except Exception as e:
        print(f"An error occured while reading CSV the file: {str(e)}.") 
    

def check_valid(row: list, patterns: dict) -> bool:
    """
    The function checks the data for compliance with regular expressions

    Args:
            row: list of data rows to check
            patterns: dictionary in which the keys are the header names 
                      and the values are regular expressions to check

    Returns: 
            bool: true if the string matches the template, otherwise false
    """
    for key, value in zip(patterns.keys(), row):
        if not re.match(patterns[key], value):
            return False
    return True


def check_data(path_csv: str, path_json: str) -> List[int]:
    """
    The function returns a list of invalid rows numbers

    Args:
            path_csv:  path to .csv file
            path_json: path to .json file

    Returns:
            List[int]: list of invalid rows numbers
    """
    data = get_csv(path_csv)
    reg_exp = get_json(path_json)
    invalid_rows = []
    for i, row in enumerate(data):
        if not check_valid(row, reg_exp):
            invalid_rows.append(i)
    return invalid_rows


if __name__ == "__main__":
    invalid = check_data(PATH_TO_CSV, PATTERNS)
    check_sum = calculate_checksum(invalid)
    serialize_result(VARIANT, check_sum)
    print(len(invalid))
     