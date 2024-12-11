import pytest
from unittest.mock import patch
from gcd import gcd, main


# Тесты для функции gcd

def test_gcd_positive_numbers():
    assert gcd(48, 18) == 6
    assert gcd(101, 103) == 1


def test_gcd_with_zero():
    assert gcd(0, 10) == 10
    assert gcd(10, 0) == 10


def test_gcd_negative_numbers():
    assert gcd(-48, 18) == 6
    assert gcd(48, -18) == 6
    assert gcd(-48, -18) == 6


# Тесты для функции main

def test_main_valid_input(capsys):
    main(["48", "18"])
    captured = capsys.readouterr()
    assert "НОД чисел 48 и 18 равен 6" in captured.out


def test_main_invalid_input(capsys):
    main(["a", "b"])
    captured = capsys.readouterr()
    assert "Ожидался ввод двух целых положительных чисел." in captured.out


def test_main_not_two_args(capsys):
    main(["10"])
    captured = capsys.readouterr()
    assert "Использование: python gcd.py x1 x2" in captured.out


# Параметризованный тест для main

@pytest.mark.parametrize("args, expected", [
    (["56", "98"], "НОД чисел 56 и 98 равен 14\n"),
    (["1000000000", "250000000"], "НОД чисел 1000000000 и 250000000 равен 250000000\n"),
    (["15", "25"], "НОД чисел 15 и 25 равен 5\n"),
])
def test_main_parametrize_valid_input(capsys, args, expected):
    main(args)
    captured = capsys.readouterr()

    assert expected in captured.out


# Тест с использованием мока для захвата sys.argv

def test_main_with_mock_argv(capsys):
    with patch('sys.argv', ['gcd', '12', '15']):
        main(['12', '15'])
        captured = capsys.readouterr()

        assert "НОД чисел 12 и 15 равен 3" in captured.out