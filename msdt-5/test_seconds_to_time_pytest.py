import pytest
from seconds_to_time import seconds_to_dhms, handle_custom_separator
from TimeInput import TimeInput

# Тесты для функции seconds_to_dhms
def test_zero_seconds():
    """Тест на вход равный 0"""
    assert seconds_to_dhms(0) == "00:00:00:00"


def test_one_day():
    """Тест на вход равный одному дню"""
    assert seconds_to_dhms(86400) == "01:00:00:00"


def test_hours_minutes_seconds():
    """Тест на вход равный 1 часу, 1 минуте и 1 секунде"""
    assert seconds_to_dhms(3661) == "00:01:01:01"


def test_large_value():
    """Тест на большое значение входа"""
    assert seconds_to_dhms(90000) == "01:01:00:00"


@pytest.mark.parametrize("invalid_input", ["тест", -100])
def test_invalid_input(invalid_input):
    """Тест на некорректный ввод (нецелое число или отрицательное значение)"""
    with pytest.raises(ValueError, match="Ввод должен быть положительным целым числом."):
        seconds_to_dhms(invalid_input)


# Тесты для функции handle_custom_separator
def test_custom_separator():
    """Тест на вход с кастомным разделителем"""
    input_str = "86400;90000;3661"
    expected_output = "01:00:00:00; 01:01:00:00; 00:01:01:01"
    assert handle_custom_separator(input_str, ";") == expected_output


def test_custom_separator_invalid_input():
    """Тест на некорректный ввод с кастомным разделителем"""
    input_str = "86400;test;3661"
    expected_output = "Ошибка: введите положительное целое число секунд"
    assert handle_custom_separator(input_str, ";") == expected_output


def test_custom_separator_negative_input():
    """Тест на отрицательное значение с кастомным разделителем"""
    input_str = "86400;-100;3661"
    expected_output = "Ошибка: введите положительное целое число секунд"
    assert handle_custom_separator(input_str, ";") == expected_output


# Тесты для класса TimeInput
def test_time_input_class():
    """Тест на создание объекта класса TimeInput и конвертацию"""
    time_input = TimeInput(86400)
    assert time_input.convert_to_dhms() == "01:00:00:00"


@pytest.mark.parametrize("invalid_input", ["тест", -100])
def test_time_input_invalid(invalid_input):
    """Тест на создание объекта класса TimeInput с некорректным значением"""
    with pytest.raises(ValueError, match="Ввод должен быть положительным целым числом."):
        TimeInput(invalid_input)

#запуск тестов - pytest C:\Users\User\PycharmProjects\MSDT1\msdt-5\test_seconds_to_time_pytest.py

