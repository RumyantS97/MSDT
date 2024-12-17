import pytest
from Lab5 import SearchElement
from Lab5 import main

def test_find_element_found():
    search = SearchElement()
    array = [1, 2, 3, 4, 5]
    target = 3
    result = search.find(array, target)
    assert result == 2, "Элемент должен быть найден на позиции 2"

def test_find_element_not_found():
    search = SearchElement()
    array = [1, 2, 3, 4, 5]
    target = 6
    result = search.find(array, target)
    assert result == -1, "Элемент не должен быть найден"

def test_find_empty_array():
    search = SearchElement()
    array = []
    target = 1
    result = search.find(array, target)
    assert result == -1, "Поиск в пустом массиве должен возвращать -1"

@pytest.mark.parametrize("input_string,expected", [
    ("1, 2, 3", [1, 2, 3]),
    (" 10 , 20,30 ", [10, 20, 30]),
    ("4", [4])
])
def test_parse_input_valid(input_string, expected):
    search = SearchElement()
    result = search.parse_input(input_string)
    assert result == expected, f"Результат должен быть {expected}"

def test_parse_input_invalid():
    search = SearchElement()
    with pytest.raises(ValueError, match="Некорректный формат входных данных."):
        search.parse_input("a, b, c")

@pytest.mark.parametrize("array,target,expected", [
    ([1, 2, 3, 4, 5], 4, 3),
    ([10, 20, 30, 40, 50], 15, -1),
    ([], 1, -1)
])
def test_find_with_parametrize(array, target, expected):
    search = SearchElement()
    result = search.find(array, target)
    assert result == expected, f"Для массива {array} и числа {target} ожидалось {expected}"

def test_main_with_mocking(mocker):
    mocker.patch('builtins.input', side_effect=["1, 2, 3", "2"])
    mock_print = mocker.patch('builtins.print')
    main()
    mock_print.assert_any_call("Элемент найден на позиции: 1")
    