import pytest
import os
from unittest import mock
from scrambler import scramble_text, scramble_file, shift_char

# Тесты для функции shift_char
@pytest.mark.parametrize("char, shift, expected", [
    ('a', 1, 'b'),
    ('z', 1, 'a'),
    ('A', 1, 'B'),
    ('Z', 1, 'A'),
    ('!', 1, '!'),
    ('b', -1, 'a'),
    ('y', 2, 'a')
])
def test_shift_char(char, shift, expected):
    """Тесты для функции shift_char с параметризацией"""
    assert shift_char(char, shift) == expected

# Тесты для функции scramble_text
@pytest.mark.parametrize("text, shift, expected", [
    ('hello', 1, 'ifmmp'),
    ('HELLO', 1, 'IFMMP'),
    ('abc XYZ', 2, 'cde ZAB'),
    ('hello, world!', 1, 'ifmmp, xpsme!'),
    ('', 1, '')
])
def test_scramble_text(text, shift, expected):
    """Тесты для функции scramble_text с параметризацией"""
    assert scramble_text(text, shift) == expected

# Тест для функции scramble_file
def test_scramble_file(tmp_path):
    """Тест для функции scramble_file с использованием временного файла"""
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.txt"

    input_text = "hello, world!"
    expected_output = "ifmmp, xpsme!"

    with input_file.open("w", encoding="utf-8") as f:
        f.write(input_text)

    scramble_file(input_file, output_file, 1)

    with output_file.open("r", encoding="utf-8") as f:
        result = f.read()

    assert result == expected_output

# Использование mock для проверки вызовов файла
@mock.patch("scrambler.scramble_text")
def test_scramble_file_mock(mock_scramble_text, tmp_path):
    """Тест для функции scramble_file с использованием mock для подмены scramble_text"""
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.txt"

    mock_scramble_text.return_value = "mocked result"

    with input_file.open("w", encoding="utf-8") as f:
        f.write("dummy data")

    scramble_file(input_file, output_file, 1)

    with output_file.open("r", encoding="utf-8") as f:
        result = f.read()

    assert result == "mocked result"
    mock_scramble_text.assert_called_once_with("dummy data", 1)

# Тест с нестандартным сдвигом
@pytest.mark.parametrize("input_text, shift, expected_output", [
    ("hello world", 3, "khoor zruog"),
    ("abc XYZ", -1, "zab WXY")
])
def test_scramble_text_non_standard_shifts(input_text, shift, expected_output, tmp_path):
    """Тесты с нестандартным сдвигом для функции scramble_file"""
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.txt"

    with input_file.open("w", encoding="utf-8") as f:
        f.write(input_text)

    scramble_file(input_file, output_file, shift)

    with output_file.open("r", encoding="utf-8") as f:
        result = f.read()

    assert result == expected_output

# Тест для пустого файла
def test_scramble_file_empty_file(tmp_path):
    """Тест для функции scramble_file с пустым входным файлом"""
    input_file = tmp_path / "empty.txt"
    output_file = tmp_path / "output.txt"

    with input_file.open("w", encoding="utf-8") as f:
        f.write("")

    scramble_file(input_file, output_file, 1)

    with output_file.open("r", encoding="utf-8") as f:
        result = f.read()

    assert result == ""

# Тест для файла с нестандартными символами
def test_scramble_file_special_chars(tmp_path):
    """Тест для функции scramble_file с символами, не входящими в алфавит"""
    input_file = tmp_path / "special_chars.txt"
    output_file = tmp_path / "output.txt"

    input_text = "1234 !@#$%^&*()_+-=[]{}|;':,.<>/?`~"
    expected_output = "1234 !@#$%^&*()_+-=[]{}|;':,.<>/?`~"

    with input_file.open("w", encoding="utf-8") as f:
        f.write(input_text)

    scramble_file(input_file, output_file, 1)

    with output_file.open("r", encoding="utf-8") as f:
        result = f.read()

    assert result == expected_output

# Тест для файла с отрицательным сдвигом
def test_scramble_file_negative_shift(tmp_path):
    """Тест для функции scramble_file с отрицательным сдвигом"""
    input_file = tmp_path / "negative_shift.txt"
    output_file = tmp_path / "output.txt"

    input_text = "khoor, zruog!"
    expected_output = "hello, world!"

    with input_file.open("w", encoding="utf-8") as f:
        f.write(input_text)

    scramble_file(input_file, output_file, -3)

    with output_file.open("r", encoding="utf-8") as f:
        result = f.read()

    assert result == expected_output
