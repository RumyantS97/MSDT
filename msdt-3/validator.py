import csv
import re
from checksum import serialize_result, calculate_checksum


class CSVValidator:
    """Класс для валидации строк в CSV-файле с использованием регулярных выражений."""

    def __init__(self):
        # Определение регулярных выражений
        self.regex_patterns = {
            "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "http_status_message": r"^\d{3}\s.+",
            "snils": r"^\d{11}$",
            "passport": r"^\d{2} \d{2} \d{6}$",
            "ip_v4": r"^\d{1,3}(\.\d{1,3}){3}$",
            "longitude": r"^-?(180|(\d{1,2}|1[0-7]\d)(\.\d{1,})?)$",
            "hex_color": r"^#[0-9a-fA-F]{6}$",
            "locale_code": r"^[a-zA-Z]+(-[a-zA-Z]+)*$",
            "time": r"^[0-2]\d:[0-5]\d:[0-5]\d(\.\d{1,6})?$"
        }

    def is_valid_row(self, row):
        """Проверяет строку на соответствие всем шаблонам регулярных выражений."""
        return all(re.match(pattern, str(row[column])) for column, pattern in self.regex_patterns.items())

    def process_csv(self, file_path):
        """Обрабатывает CSV-файл и возвращает индексы некорректных строк."""
        invalid_rows = []
        with open(file_path, mode='r', encoding='utf-16', newline='') as file:
            reader = csv.DictReader(file, delimiter=';')
            for index, row in enumerate(reader):
                if not self.is_valid_row(row):
                    invalid_rows.append(index)
        return invalid_rows

    def run(self, file_path, result_id):
        """Основной метод для обработки CSV и сериализации результата."""
        invalid_rows_indices = self.process_csv(file_path)
        serialize_result(result_id, calculate_checksum(invalid_rows_indices))


if __name__ == "__main__":
    validator = CSVValidator()
    validator.run('81.csv', 81)
