import csv
import re

import checksum


# Define regular expressions for data patterns
TELEPHONE_PATTERN = r'\+7-\(\d{3}\)-\d{3}-\d{2}-\d{2}'
STATUS_PATTERN = r'\d{3}\ [A-Za-z\ \,]{1,}'
SNILS_PATTERN = r'\d{11}'
ID_PATTERN = r'\d{2}-\d{2}/\d{2}'
IPV4_PATTERN = (
    r'(25[0-5]|2[0-4][0-9]|1\d{2}|[1-9][0-9]|[0-9])\.'
    r'(25[0-5]|2[0-4][0-9]|1\d{2}|[1-9][0-9]|[0-9])\.'
    r'(25[0-5]|2[0-4][0-9]|1\d{2}|[1-9][0-9]|[0-9])\.'
    r'(25[0-5]|2[0-4][0-9]|1\d{2}|[1-9][0-9]|[0-9])'
)
LONGITUDE_PATTERN = r'-?\d{1,3}\.\d+'
BLOOD_TYPE_PATTERN = r'(A|B|AB|O)[−+]'
ISBN_PATTERN = r'(\d+-\d+-\d+-\d+-\d+)|(\d+-\d+-\d+-\d+)'
LOCALE_CODE_PATTERN = r'[a-z]{2}(-[a-z]{2})?'
DATE_PATTERN = (
    r'(19|20)[0-9]{2}-(1[0-2]|0[1-9])-(3[0-1]|[1-2][0-9]|0[1-9])'
)
PATTERNS = [
    TELEPHONE_PATTERN, STATUS_PATTERN, SNILS_PATTERN, ID_PATTERN,
    IPV4_PATTERN, LONGITUDE_PATTERN, BLOOD_TYPE_PATTERN,
    ISBN_PATTERN, LOCALE_CODE_PATTERN, DATE_PATTERN
]


def check_row_format(line, patterns):
    """Check if a row matches the specified patterns."""
    for i in range(10):
        if re.fullmatch(patterns[i], line[i]) is None:
            return False
    return True


# Read and process the CSV file
with open(file='66.csv', encoding='utf16') as csvfile:
    reader = csv.reader(csvfile, delimiter=";")
    all_lines = list(reader)
    incorrect_lines = []

    # Check 10,000 rows for pattern compliance
    for line_index in range(1, 10001):
        if not check_row_format(all_lines[line_index], PATTERNS):
            incorrect_lines.append(line_index - 1)

# Serialize the result
checksum.serialize_result(66, checksum.calculate_checksum(incorrect_lines))
