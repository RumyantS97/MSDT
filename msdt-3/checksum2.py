import json
import hashlib
from typing import List


def calculate_checksum(invalid_row_numbers: List[int]) -> str:
    """
    Функция для вычисления контрольной суммы на основе номеров некорректных строк.

    :param invalid_row_numbers: список номеров некорректных строк
    :return: контрольная сумма в виде строки
    """

    # Преобразуем список в строку и вычисляем его хеш
    checksum_string = ''.join(map(str, invalid_row_numbers))
    return hashlib.sha256(checksum_string.encode()).hexdigest()
