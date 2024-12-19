from functions import read_csv, read_json, get_list
from paths import CSV, PATTERNS
from checksum import calculate_checksum, serialize_result


file = read_csv(CSV)
patterns = read_json(PATTERNS)
result = get_list(file, patterns)
final_result = calculate_checksum(result)
serialize_result(9, final_result)