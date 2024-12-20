import csv
import re
from typing import Iterable

from checksum import (
    calculate_checksum,
    serialize_result
)


def is_row_valid(row: dict[str, str]):
    processors = {
        # operators.1947@protonmail.com, relate1878@sub.domain.ru
        # Типичный имейл. Состоит из латинских букв, цифр, символов "." и "@". Обратите внимание, что адрес может иметь поддомен.
        "email": r"\w+@\w+\.\w+",
        # 200 OK, 226 IM Used
        # Статус должен начинаться с трехзначного кода, отделенного пробелом от текстового описания.
        "http_status_message": r"\d{3} .+",
        # 66048764725
        # СНИЛС состоит из 11 цифровых символов. В данном задании символы СНИЛС указаны подряд без пробелов/тире и т.д.
        "snils": r"\d{11}",
        # 27 17 117724
        # В данном задании пробелами разделены первые 2 и последние 2 цифры серии, а также серия и номер паспорта.
        "passport": r"\d{2} \d{2} \d{6}",
        # 19.121.223.58
        # IP-адрес указывается без маски подсети. Не забывайте, что он 32-битный.
        "ip_v4": r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
        # -8.287791, 32.223374
        # Это долгота в системе координат WGS84 (srid 4326). Обратите внимание на ограничения на значение, которые она имеет. Должна быть числовым значением без единиц измерения и прочей текстовой информации.
        "longitude": r"-?((180\.?0*$)|(((1[0-7][0-9])|([0-9]{0,2}))\.?[0-9]*$))",
        # #d8346b
        # Это представление веб-цвета в виде трех пар 16-ричных цифр. Наличие хештега перед ними обязательно.
        "hex_color": r"#[\dabcdef]{6}",
        # 018-1-50114-053-6
        # 13-значный международный стандартный книжный номер
        "isbn": r"(\d{3}-)?\d-\d{5}-\d{3}-\d",
        # 3a7fb1ca-bdc6-4314-ad9a-6370f7a9657b
        # Код локали
        "locale_code": r"[a-z]{2}(-[a-z]{2})?",
        # 18:24:12.734883
        # Время определенного формата с указанием часов, минут и секунд с точностью до 6 знаков. Не забывайте, что в сутках 24 часа, а в минуте - 60 секунд.
        "time": r"(?:2[0-4]|[01]\d):[0-6]\d:[0-6]\d.\d{6}",
    }
    for field_name, processor in processors.items():
        if re.fullmatch(processor, row[field_name]) is None:
            return False
    return True


def get_wrong_lines() -> Iterable[int]:
    with open("1.csv", mode="r", encoding="utf16", newline="") as file_to_validate:
        strings_reader = csv.DictReader(file_to_validate, delimiter=';')
        for i, row in enumerate(strings_reader):
            if not is_row_valid(row):
                yield i


def main():
    lines = list(get_wrong_lines())
    variant = 1
    checksum = calculate_checksum(lines)
    serialize_result(variant, checksum)


if __name__ == '__main__':
    main()
