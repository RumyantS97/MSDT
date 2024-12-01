import csv
import re
import os
import json
from checksum import calculate_checksum, serialize_result


REGEX_PATTERNS = {"telephone": r"^\+7-\(\d{3}\)-\d{3}-\d{2}-\d{2}$",
                  "http_status_message": r"^\d{3}\s[A-Za-z ]+$",
                  "inn": r"^\d{12}$",
                  "identifier": r"^\d{2}-\d{2}/\d{2}$",
                  "ip_v4": r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
                  "latitude": r"^-?90(\.0+)?$|^-?[0-9]{1,2}(\.[0-9]+)?$",
                  "blood_type": r"^[A-B]?([AB])\+?|O[\-+]$",
                  "isbn": r"^\d{3}-\d-\d{3}-\d{3}-\d$",
                  "uuid": r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$",
                  "date": r"^(?:\d{4})-(?:0[1-9]|1[0-2])-(?:[012]\d|3[01])$" }
                  
                  
def is_valid_row(row: list[str]) -> bool:
    """
    Checks if a row of data matches the predefined patterns.

    :param row: A list of strings representing the values in a CSV row.

    :return: True if all values in the row match the patterns, False otherwise.
    """
    return all(re.match(pattern, value) for pattern, value in zip(REGEX_PATTERNS.values(), row))


def get_invalid_rows(csv_file: str) -> list[int]:
    """
    Returns a list of indices of invalid rows in a CSV file.

    :param csv_file: The path to the CSV file.

    :return: A list of indices (starting from 0) of rows that do not match the specified patterns.
             An empty list if the file is not found or an error occurs during processing.
    """
    invalid_rows = []
    try:
        with open(csv_file, "r", newline="", encoding="utf-16") as file:
            reader = csv.reader(file, delimiter=";")
            # Skip the header
            next(reader, None)
            for i, row in enumerate(reader):
                if not is_valid_row(row):
                    invalid_rows.append(i)
    except FileNotFoundError:
        print(f"Error: File {csv_file} not found.")
        #Return an empty list on error
        return []
    except Exception as e:
        print(f"An error occurred during file processing: {e}")
        #Return an empty list on error
        return []

    return invalid_rows


def write_results_to_json(variant: int, checksum: str, output_file: str = "result.json") -> None:
    """
    Writes the variant and checksum to a JSON file.

    :param variant: The variant number.
    :param checksum: The calculated checksum.
    :param output_file: The path to the output JSON file (default: "result.json").
    """
    result = {"variant": str(variant), "checksum": checksum}
    try:
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(result, json_file, indent=4)
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")
        

if __name__ == "__main__":
    csv_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "14.csv")
    invalid_rows = get_invalid_rows(csv_file)
    checksum = calculate_checksum(invalid_rows)
    # serialize_result(14, checksum)
    write_results_to_json(14, checksum)
    print(checksum)