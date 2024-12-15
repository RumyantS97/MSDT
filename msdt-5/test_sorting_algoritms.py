import random
import pytest
from unittest.mock import patch

# Импорт функций
from main import (
    bubble_sort, cocktail_shaker_sort, insertion_sort, quick_sort, heap_sort, bucket_sort
)

# Проверка корректной работы всех алгоритмов сортировки на различных входных данных
@pytest.mark.parametrize("sort_func, input_data, expected", [
    (bubble_sort, [4, 2, 7, 1], [1, 2, 4, 7]),
    (cocktail_shaker_sort, [3, 3, 2, 1], [1, 2, 3, 3]),
    (insertion_sort, [10, -1, 2, 5], [-1, 2, 5, 10]),
    (quick_sort, [8, 4, 2, 6], [2, 4, 6, 8]),
    (heap_sort, [9, 7, 5, 3], [3, 5, 7, 9]),
    (bucket_sort, [0.9, 0.5, 0.1, 0.7], [0.1, 0.5, 0.7, 0.9]),
])
def test_sorting_algorithms(sort_func, input_data, expected):
    # Утверждение, что функция сортировки возвращает правильный результат
    assert sort_func(input_data) == expected

# Проверка корректной обработки пустого массива для всех сортировок
@pytest.mark.parametrize("sort_func", [bubble_sort, cocktail_shaker_sort, insertion_sort, quick_sort, heap_sort])
def test_empty_array(sort_func):
    assert sort_func([]) == []

# Проверка корректной обработки массива с одним элементом
@pytest.mark.parametrize("sort_func", [bubble_sort, cocktail_shaker_sort, insertion_sort, quick_sort, heap_sort])
def test_single_element_array(sort_func):
    assert sort_func([1]) == [1]

# Проверка работы алгоритмов на уже отсортированном массиве
@pytest.mark.parametrize("sort_func", [bubble_sort, cocktail_shaker_sort, insertion_sort, quick_sort, heap_sort])
def test_already_sorted_array(sort_func):
    assert sort_func([1, 2, 3, 4]) == [1, 2, 3, 4]

# Проверка работы алгоритмов на массиве, отсортированном в обратном порядке
@pytest.mark.parametrize("sort_func", [bubble_sort, cocktail_shaker_sort, insertion_sort, quick_sort, heap_sort])
def test_reverse_sorted_array(sort_func):
    assert sort_func([4, 3, 2, 1]) == [1, 2, 3, 4]

# Проверка сортировки больших случайных массивов (наиболее эффективных алгоритмов)
@pytest.mark.parametrize("sort_func", [quick_sort, heap_sort])
def test_large_random_array(sort_func):
    large_array = [random.randint(0, 1000) for _ in range(1000)]
    assert sort_func(large_array) == sorted(large_array)

def test_bucket_sort_negative():
    """
    Проверка обработки ошибки при попытке сортировать массив с отрицательными числами
    в блочной сортировке. Ожидается, что будет выброшено исключение ValueError.
    """
    with pytest.raises(ValueError):
        bucket_sort([-0.5, 0.2, 0.1])  # Блочная сортировка не поддерживает отрицательные числа

# Проверка корректной работы быстрой сортировки с дубликатами элементов
def test_quick_sort_duplicates():
    array = [5, 1, 5, 2, 2, 5, 1]
    assert quick_sort(array) == sorted(array)

# Проверка работы пирамидальной сортировки со строками
def test_heap_sort_with_strings():
    array = ["b", "a", "c"]
    assert heap_sort(array) == ["a", "b", "c"]

# Проверка внутренней реализации блочной сортировки с использованием mock для алгоритма сортировки вставками
@patch("main.insertion_sort")
def test_bucket_sort_mocked_insertion(mock_insertion):
    mock_insertion.side_effect = lambda x: sorted(x)  # Вставляем фейковую сортировку
    result = bucket_sort([0.8, 0.2, 0.5, 0.3])
    assert result == [0.2, 0.3, 0.5, 0.8]
    assert mock_insertion.call_count > 0  # Проверяем, что insertion_sort был вызван

# Интеграционный тест: проверка взаимодействия генерации случайных чисел и основной функции программы
@patch("main.random.randint", return_value=50)
def test_main_random_generation(mock_randint):
    from main import main
    with patch("builtins.input", side_effect=["4", "2"]):  # Мокируем ввод пользователя
        with patch("builtins.print") as mock_print:  # Мокируем вывод в консоль
            main()
            mock_print.assert_any_call("Сгенерированный массив: ", [50, 50, 50, 50]) # Проверяем корректный вывод