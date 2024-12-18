import csv
import re
from checksum import serialize_result, calculate_checksum


class CSVValidator:
    """Класс для валидации строк в CSV-файле с использованием регулярных выражений."""

    def __init__(self):
        # Определение регулярных выражений
        self.regex_patterns = {
            "telephone": r"^\+7-\(\d{3}\)-\d{3}-\d{2}-\d{2}$",
            "height": r"^[1-2]\.\d{2}$",
            "inn": r"^\d{12}$",
            "identifier": r"^\d{2}-\d{2}/\d{2}$",
            "occupation": r"^[A-Za-zА-Яа-яёЁ\s-]+$",
            "latitude": r"^-?\d{1,2}\.\d+$",
            "blood_type": r"^(A|B|AB|O)[+-]$",
            "issn": r"^\d{4}-\d{4}$",
            "uuid": r"^[a-f0-9\-]{36}$",
            "date": r"^\d{4}-\d{2}-\d{2}$"
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
    validator.run('80.csv', 80)
