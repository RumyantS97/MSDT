import os
import unittest
from unittest.mock import mock_open, patch

from parameterized import parameterized

from msdt_project5 import TrimSpaces

class TestTrimSpaces(unittest.TestCase):
    def read_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()

    # Тест 1: Проверка удаления лишних пробелов в строках и файлах
    def test_trim_spaces_from_file_and_string(self):
        input_text = " Это пример текста с лишними пробелами "
        expected_output = "Это пример текста с лишними пробелами"

        # Тест 1.1: Проверка обработки строки
        result = TrimSpaces.trim_extra_spaces(input_text)
        self.assertEqual(expected_output, result)

        # Тест 1.2: Проверка обработки файла с пробелами и табуляциями
        content = "  Это    пример\tтекста с пробелами и табуляциями  "
        with open("test.txt", 'w', encoding='utf-8') as file:
            file.write(content)

        file_content = self.read_file("test.txt")
        expected_file_output = "Это пример текста с пробелами и табуляциями"
        file_result = TrimSpaces.trim_extra_spaces(file_content)
        self.assertEqual(expected_file_output, file_result)

        os.remove("test.txt")

    # Тест 2: Проверка обработки строки с пробелами через консоль с кодировкой UTF-8
    def test_trim_spaces_with_encoding(self):
        input_text = " Это пример текста с лишними пробелами "
        expected_output = "Это пример текста с лишними пробелами"

        result = TrimSpaces.trim_extra_spaces(input_text)

        self.assertEqual(expected_output, result)

    # Тест 3: Проверка обработки пустых строк
    def test_empty_file_and_string(self):
        input_text = "     "
        expected_output = ""

        # Тест 2.1: Проверка обработки строки из пробелов
        result = TrimSpaces.trim_extra_spaces(input_text)
        self.assertEqual(expected_output, result)

        # Тест 2.2: Проверка пустого файла (файл состоит только из пробелов)
        with open("empty.txt", 'w', encoding='utf-8') as file:
            file.write("     ")

        file_content = self.read_file("empty.txt")
        file_result = TrimSpaces.trim_extra_spaces(file_content)
        self.assertEqual(expected_output, file_result)

        os.remove("empty.txt")

    # Тест 4: Проверка обработки больших файлов
    def test_large_file_handling(self):
        large_content = " Это\tпример " * 1000000
        with open("large_text.txt", 'w', encoding='utf-8') as file:
            file.write(large_content)

        file_content = self.read_file("large_text.txt")

        result = TrimSpaces.trim_extra_spaces(file_content)

        expected_output = " ".join(["Это пример"] * 1000000)

        self.assertEqual(expected_output, result)

        os.remove("large_text.txt")

    # Тест 5: Параметризованный тест
    @parameterized.expand([
        ("simple_case", " Это пример текста ", "Это пример текста"),
        ("tabs_and_spaces", "  Это\tпример текста\t ", "Это пример текста"),
        ("multiple_spaces", "  Пример  с   пробелами   внутри  ", "Пример с пробелами внутри"),
        ("empty_string", "", ""),
        ("only_spaces", "     ", "")
    ])
    def test_trim_spaces_parameterized(self, name, input_text, expected_output):
        result = TrimSpaces.trim_extra_spaces(input_text)
        self.assertEqual(expected_output, result, f"Failed for case: {name}")

    # Тест 6: Использование моков
    @patch("builtins.open", new_callable=mock_open, read_data="  Это    пример\tтекста с пробелами и табуляциями  ")
    def test_trim_spaces_with_mock_file(self, mock_file):
        with open("mock_file.txt", 'r', encoding='utf-8') as file:
            content = file.read()

        result = TrimSpaces.trim_extra_spaces(content)

        expected_output = "Это пример текста с пробелами и табуляциями"

        self.assertEqual(expected_output, result)
        mock_file.assert_called_once_with("mock_file.txt", 'r', encoding='utf-8')

    # Тест 7: Проверка строки с табуляциями и пробелами
    def test_trim_tabs_and_spaces_only(self):
        input_text = "\t  \t   "
        expected_output = ""

        result = TrimSpaces.trim_extra_spaces(input_text)

        self.assertEqual(expected_output, result)
