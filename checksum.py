import json
import hashlib
from typing import List

def calculate_checksum(row_numbers: List[int]) -> str:
    row_numbers.sort()
    return hashlib.md5(json.dumps(row_numbers).encode('utf-8')).hexdigest()


def serialize_result(variant: int, checksum: str) -> None:

    result={
        "variant":str(variant),
        "checksum": checksum
    }
    with open('result.json', 'w') as file:
        json.dump(result, file)