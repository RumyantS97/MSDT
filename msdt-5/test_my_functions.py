import pytest
from unittest.mock import patch
from my_functions import add, subtract, multiply, divide, square, greet, fetch_data

def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(5, 3) == 2

def test_multiply():
    assert multiply(4, 5) == 20

def test_divide():
    assert divide(10, 2) == 5
    with pytest.raises(ValueError):
        divide(10, 0)

def test_square():
    assert square(3) == 9

def test_greet():
    assert greet("Alice") == "Hello, Alice!"

@patch('my_functions.requests.get')
def test_fetch_data(mock_get):
    # Настраиваем мок для возврата определенного значения
    mock_get.return_value.json.return_value = {"key": "value"}

    result = fetch_data("http://fakeapi.com/data")

    assert result == {"key": "value"}
    mock_get.assert_called_once_with("http://fakeapi.com/data")

@patch('my_functions.requests.get')
def test_fetch_data_error(mock_get):
    # Настраиваем мок для имитации ошибки
    mock_get.side_effect = Exception("Network error")

    with pytest.raises(Exception) as e:
        fetch_data("http://fakeapi.com/data")

    assert str(e.value) == "Network error"
