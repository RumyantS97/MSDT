import pytest
from unittest.mock import patch
from lab5 import DivisionResult, parse_integer, divide, read_menu, main

# Тесты для функции read_menu
def test_read_menu_valid():
    assert read_menu("1") == "1"
    assert read_menu("2") == "2"

def test_read_menu_invalid():
    with pytest.raises(ValueError,
                       match="Ошибка: Введён неверный пункт меню."):
        read_menu("10")
    with pytest.raises(ValueError,
                       match="Ошибка: Введён неверный пункт меню."):
        read_menu("ahjdh2")

# Тесты для функции parse_integer
def test_parse_integer_valid():
    assert parse_integer("123") == 123
    assert parse_integer("-123") == -123
    assert parse_integer("  42  ") == 42

def test_parse_integer_invalid():
    with pytest.raises(
            ValueError,
            match="Ошибка: Введённая строка не является целым числом."):
        parse_integer("abc")
    with pytest.raises(
            ValueError,
            match="Ошибка: Введённая строка не является целым числом."):
        parse_integer("")
    with pytest.raises(
            ValueError,
            match="Ошибка: Введённая строка не является целым числом."):
        parse_integer("12.3")

# Параметризованный тест для функции divide
@pytest.mark.parametrize("x, y, expected_q, expected_r", [
    (0, 3, 0, 0),         # x = 0
    (10, 3, 3, 1),        # x > 0, y > 0
    (10, -3, -3, 1),      # x > 0, y < 0
    (-10, 3, -4, 2),      # x < 0, y > 0
    (-10, -3, 4, 2),      # x < 0, y < 0
])
def test_divide(x, y, expected_q, expected_r):
    result = divide(x, y)
    assert result.q == expected_q
    assert result.r == expected_r

# Тест с моками для проверки завершения работы
def test_main_menu_option_2():
    with patch("builtins.input", side_effect=["2"]):
        with patch("builtins.print") as mock_print:
            main()
            mock_print.assert_called_with("Завершение работы...")

# Тест с моками для проверки исключения y = 0
def test_main_division_by_zero():
    with patch("builtins.input",
               side_effect=["1", "25", "0", "156", "2"]):
        with patch("builtins.print") as mock_print:
            main()
            mock_print.assert_any_call("Делитель не может быть равен 0!")