import pytest
import lab5


# Параметризованное тестирование
@pytest.mark.parametrize("test_input,expected", [(3, 6), (4, 24), (5, 120)])
def test_factorial(test_input, expected):
    assert lab5.factorial(5) == 120


def test_check_duplicate_false():
    assert lab5.check_duplicate([1, 2, 3]) is False


def test_check_duplicate_true():
    assert lab5.check_duplicate([1, 2, 2, 3]) is True


# Использование stub
def test_get_phone_and_address_by_id():
    def stub_db_connection(client_id):  # Создаём stub для функции
        return [1, 'name', 'address', 'phone']
    lab5.db_connection = stub_db_connection  # Заменяем функцию на stub
    assert lab5.get_phone_and_address_by_id(1) == "Phone: phone, " \
                                                  "Address: address"


def test_palindrome_true():
    assert lab5.palindrome('aba') is True


# Проверка на вывод ошибки
def test_palindrome_exception():
    with pytest.raises(Exception) as exception:
        lab5.palindrome('')
    assert 'empty input' == str(exception.value)


@pytest.fixture
def matrix():
    matrix = []
    number = 1
    for i in range(3):
        matrix.append([])
        for j in range(3):
            matrix[i].append(number)
            number += 1
    return matrix


# Использование fixture
def test_transpose(matrix):
    assert lab5.transpose(matrix) == [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
