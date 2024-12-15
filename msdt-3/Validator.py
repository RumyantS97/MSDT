"""
Class Validator

This module validate data for some regex pattern
"""

# Import match for matching strings to regex
from re import match


VALID_HTTP_STATUS_REGEX = r"^[1-5]\d{2}\s[A-Za-z]"
VALID_EMAIL_REGEX = r"^\w+@\w+(\.\w+)+$"
VALID_INN_REGEX = r"^\d{12}$"
VALID_PASSPORT_REGEX = r"^\d{2}\s\d{2}\s\d{6}$"
VALID_IPV4_REGEX = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
VALID_LATITUDE_REGEX = r"^[-\d]\d*(\.\d+)?$"
VALID_RGB_REGEX = r"^#[\dA-Fa-f]{6}$"
VALID_ISBN_REGEX = r"(^\d{3}-)?\d-\d{5}-\d{3}-\d$"
VALID_UUID_REGEX = (
    r"^[\da-fA-F]{8}-[\da-fA-F]{4}-[\da-fA-F]{4}-[\da-fA-F]{4}-[\da-fA-F]{12}$"
)

VALID_TIME_REGEX = r"^([0-1][0-9]|[2][0-3]):[0-5][0-9]:[0-5][0-9]\.[0-9]{6}$"


MIN_LATITUDE = -90
MAX_LATITUDE = 90


class Validator:
    def __init__(self):
        pass

    def is_http_status_valid(self, input_status: str) -> bool:
        return match(VALID_HTTP_STATUS_REGEX, input_status) is not None

    def is_email_valid(self, input_email: str) -> bool:
        return match(VALID_EMAIL_REGEX, input_email) is not None

    def is_inn_valid(self, input_inn: str) -> bool:
        return match(VALID_INN_REGEX, input_inn) is not None

    def is_passport_valid(self, input_password: str) -> bool:
        return match(VALID_PASSPORT_REGEX, input_password) is not None

    def is_ipv4_valid(self, input_ip: str) -> bool:
        return match(VALID_IPV4_REGEX, input_ip) is not None

    def is_latitude_valid(self, input_latitude: str) -> bool:
        if match(VALID_LATITUDE_REGEX, input_latitude) is not None:
            latitude = float(input_latitude)
            return MIN_LATITUDE <= latitude <= MAX_LATITUDE
        else:
            return False

    def is_rgb_valid(self, input_rgb: str) -> bool:
        return match(VALID_RGB_REGEX, input_rgb) is not None

    def is_isbn_valid(self, input_isbn: str) -> bool:
        return match(VALID_ISBN_REGEX, input_isbn) is not None

    def is_uuid_valid(self, input_uuid: str) -> bool:
        return match(VALID_UUID_REGEX, input_uuid) is not None

    def is_time_valid(self, input_time: str) -> bool:
        return match(VALID_TIME_REGEX, input_time) is not None
