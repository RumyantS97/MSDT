import pytest
from unittest.mock import patch

# Импортируем функцию, которую будем тестировать
from main import kmh_to_mps, main

# Тест для функции kmh_to_mps
def test_kmh_to_mps():
    assert kmh_to_mps(36) == 10.0
    assert kmh_to_mps(72) == 20.0
    assert kmh_to_mps(108) == 30.0

# Параметризованный тест для функции kmh_to_mps
@pytest.mark.parametrize("speed_kmh, expected_mps", [
    (36, 10.0),
    (72, 20.0),
    (126, 35.0),
    (18, 5.0),
    (108, 30.0)
])
def test_kmh_to_mps_parametrized(speed_kmh, expected_mps):
    assert kmh_to_mps(speed_kmh) == expected_mps

# Тест для функции main с использованием моков
@patch('builtins.input', side_effect=['1', '36', '2'])
@patch('builtins.print')
def test_main(mock_print, mock_input):
    main()
    mock_print.assert_any_call("36.0 км/ч = 10.00 м/с")
    mock_print.assert_any_call("Завершение работы программы.")

# Тест для функции main с некорректным вводом
@patch('builtins.input', side_effect=['1', 'invalid', '2'])
@patch('builtins.print')
def test_main_invalid_input(mock_print, mock_input):
    main()
    mock_print.assert_any_call("Ошибка: Введите корректное числовое значение.")
    mock_print.assert_any_call("Завершение работы программы.")

# Тест для функции main с отрицательным числом
@patch('builtins.input', side_effect=['1', '-10', '2'])
@patch('builtins.print')
def test_main_negative_input(mock_print, mock_input):
    main()
    mock_print.assert_any_call("Ошибка: Скорость должна быть положительным числом.")
    mock_print.assert_any_call("Завершение работы программы.")

# Тест для функции main с выбором завершения работы
@patch('builtins.input', side_effect=['2'])
@patch('builtins.print')
def test_main_exit(mock_print, mock_input):
    main()
    mock_print.assert_any_call("Завершение работы программы.")

# Тест для функции main с несколькими итерациями конвертации
@patch('builtins.input', side_effect=['1', '36', '1', '72', '2'])
@patch('builtins.print')
def test_main_multiple_conversions(mock_print, mock_input):
    main()
    mock_print.assert_any_call("36.0 км/ч = 10.00 м/с")
    mock_print.assert_any_call("72.0 км/ч = 20.00 м/с")
    mock_print.assert_any_call("Завершение работы программы.")