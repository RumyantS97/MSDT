import sys
import io
import pytest
from unittest.mock import patch
import sorting


# Параметризованный тест для проверки работоспособности кастомных операторов
@pytest.mark.parametrize("a,b", [(1, 4), (8, 8), (9, 2)])
def test_operators_parametrize(a, b):
    assert sorting.operator_gt(a, b) == (a > b)
    assert sorting.operator_ge(a, b) == (a >= b)
    assert sorting.operator_lt(a, b) == (a < b)
    assert sorting.operator_le(a, b) == (a <= b)
    assert sorting.operator_ne(a, b) == (a != b)
    assert sorting.operator_eq(a, b) == (a == b)


# Тест проверяющий вывод массива длиной <= 40
def test_display_short_array():
    array = list(range(1, 40))
    # Перехватываем вывод в консоль и возвращаем обратно
    output_capture = io.StringIO()
    sys.stdout = output_capture
    sorting.display_array(array)
    sys.stdout = sys.__stdout__
    # Получаем последнюю выведенную строку
    output = output_capture.getvalue().strip().split('\n')[-1]
    # Короткий массив должен вывестись весь без изменений
    expected_output = array.__str__()
    assert output == expected_output


# Тест проверяющий вывод массива длиной > 40
def test_display_long_array():
    array = list(range(1, 41))
    # Перехватываем вывод в консоль и возвращаем обратно
    output_capture = io.StringIO()
    sys.stdout = output_capture
    sorting.display_array(array)
    sys.stdout = sys.__stdout__
    # Получаем последнюю выведенную строку
    output = output_capture.getvalue().strip().split('\n')[-1]
    # Должны вывестись первые и последние 20 элементов через многоточие
    expected_output = '['
    for i in array[:20]:
        expected_output += f"{i}, "
    expected_output += "'...'"
    for i in array[-20:]:
        expected_output += f", {i}"
    expected_output += ']'
    assert output == expected_output


@pytest.mark.parametrize("sorting_method", [sorting.cocktail_sort,
                                            sorting.selection_sort,
                                            sorting.bubble_sort,
                                            sorting.comb_sort,
                                            sorting.gnome_sort,
                                            sorting.insertion_sort,
                                            ])
def test_sorting_asc(sorting_method):
    src_arr = list(range(100, 1))
    expected_arr = src_arr.copy()
    actual_arr = src_arr.copy()

    expected_arr.sort()
    sorting_method(actual_arr, True)
    assert actual_arr == expected_arr


@pytest.mark.parametrize("sorting_method", [sorting.cocktail_sort,
                                            sorting.selection_sort,
                                            sorting.bubble_sort,
                                            sorting.comb_sort,
                                            sorting.gnome_sort,
                                            sorting.insertion_sort,
                                            ])
def test_sorting_desc(sorting_method):
    src_arr = list(range(1, 100))
    expected_arr = src_arr.copy()
    actual_arr = src_arr.copy()

    expected_arr.sort(reverse=True)
    sorting_method(actual_arr, False)
    assert actual_arr == expected_arr


# Быстрая сортировка вынесена из общего теста, тк не изменяет
# исходный массив, а возвращает отсортированный результат
@pytest.mark.parametrize("order", [True, False])
def test_quick_sorting_asc(order):
    src_arr = list(range(100, 1)) + list(range(1, 100))
    expected_arr = src_arr.copy()
    expected_arr.sort(reverse=order)

    assert sorting.quicksort(src_arr, not order) == expected_arr


# Тест, проверяющий валидацию на ввод в функцию select_type_sort
# Параметры разделены на блоки:
# 1. Корректный ввод в оба поля (по граничным значениям)
# 2. Некорректный ввод (по границам и типу) в первое, корректный во второе
# 3. Корректный ввод в первое, некорректный (по границам и типу) во второе
@pytest.mark.parametrize("input_,expected_output", [([1, 1], (1, 1)),
                                                    ([7, 2], (7, 2)),

                                                    ([-1, 2, 1], (2, 1)),
                                                    ([8, 3, 1], (3, 1)),
                                                    (['asd', 4, 1], (4, 1)),

                                                    ([5, -1, 6, 2], (6, 2)),
                                                    ([7, 3, 5, 1], (5, 1)),
                                                    ([1, 'asd', 5, 2], (5, 2)),
                                                    ])
def test_select_sorting_type(input_, expected_output):
    with patch('builtins.input', side_effect=input_):
        result = sorting.select_type_sort()
        assert result == expected_output
