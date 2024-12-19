import csv
import re
from typing import List, Dict
from REGEX_PATTERNS import REGEX_PATTERNS
from checksum import serialize_result, calculate_checksum


def is_valid_row(row: Dict[str, str], regex_patterns: Dict[str, str]) -> bool:
    """
    Check if a row matches all regex patterns.

    Args:
        row (Dict[str, str]): A dictionary representing a row in the CSV file.
        regex_patterns (Dict[str, str]): A dictionary of regex patterns.

    Returns:
        bool: True if the row matches all patterns, False otherwise.
    """
    return all(re.match(pattern, str(row[column])) for column, pattern in regex_patterns.items())


def process_csv(file_path: str, regex_patterns: Dict[str, str]) -> List[int]:
    """
    Process a CSV file and return the indices of invalid rows.

    Args:
        file_path (str): The path to the CSV file.
        regex_patterns (Dict[str, str]): A dictionary of regex patterns.

    Returns:
        List[int]: A list of indices of invalid rows.
    """
    invalid_rows: List[int] = []
    with open(file_path, mode='r', encoding='utf-16', newline='') as file:
        reader = csv.DictReader(file, delimiter=';')
        for index, row in enumerate(reader):
            if not is_valid_row(row, regex_patterns):
                invalid_rows.append(index)
    return invalid_rows


def run_validation(file_path: str, result_id: int):
    """
    Run the CSV validation process and serialize the result.

    Args:
        file_path (str): The path to the CSV file.
        result_id (int): The ID to use for serializing the result.
    """
    invalid_rows_indices = process_csv(file_path, REGEX_PATTERNS)
    serialize_result(result_id, calculate_checksum(invalid_rows_indices))


if __name__ == "__main__":
    run_validation('82.csv', 82)