"""class validator. This module validate data for some regex pattern."""
# Import match for matching strings to regex
from re import match


patterns = {
    "http_status" : r"^[1-5]\d{2}\s[A-Za-z]",
    # email can be with zero domain like a@ssau.ru.
    "email"       : r"^\w+@(\w+\.?)+$",
    "passport"    : r"^\d{2}\s\d{2}\s\d{6}$",
    "hex_color"         : r"^#[\dA-Fa-f]{6}$",
    "time"        : r"^([0-1][0-9]|[2][0-3]):[0-5][0-9]:[0-5][0-9]\.[0-9]{6}$",
    "height"      : r"^[0-2]\.\d{2}$",  # рост
    "snils"       : r"^\d{11}$",  # снилс
    "occupation"  : r"^[A-Za-zА-Яа-я- ]+$",  # профессия
    "longitude"   : r"^[(\-\d)\d]\d*\.\d*$",  # долгота
    "issn"        : r"^\d{4}\-\d{4}$",  # issn 
    "locale_code" : r"^[A-Za-z]+(\-[A-Za-z]+)*$",  # locale code
}

MAX_LONGITUDE = 180
MIN_LONGITUDE = -180

class Validator:
    """Validator (class with methods for validating data."""

    def __init__(self):
        pass

    def validate_data(self, regex_pattern: str, input_data: str) -> bool:
        """Validate data for pattern.

        Args:
            regex_pattern (str): chosen pattern
            input_data (str): data for validation.

        Returns:
            bool: True if data in right format, else false.

        """
        # check if pattern in patterns
        if regex_pattern not in patterns:
            return False

        # return is data in right format
        # match return class <'re.Match'> if format is true
        # and return <NoneType> else
        # thats wy we use [is not None]
        return match(patterns[regex_pattern], input_data) is not None
