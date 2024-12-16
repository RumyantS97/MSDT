import pytest
from main import segment_replace, main
from unittest.mock import patch


def test_segment_replace_valid_case():
    input_array = [1, 2, 3, 4, 5, 6]
    result = segment_replace(input_array, 2, 3, 5, 6)
    assert result == [1, 5, 6, 4, 2, 3], "Ошибка: сегменты переставлены неверно"


def test_segment_replace_invalid_boundaries_a1_b1():
    input_array = [1, 2, 3, 4, 5]
    with pytest.raises(Exception, match="Не удалось создать файл с результатом"):
        segment_replace(input_array, 3, 2, 4, 5)


def test_segment_replace_invalid_boundaries_a2_b2():
    input_array = [1, 2, 3, 4, 5]
    with pytest.raises(Exception, match="Не удалось создать файл с результатом"):
        segment_replace(input_array, 1, 2, 5, 4)


def test_segment_replace_out_of_bounds():
    input_array = [1, 2, 3, 4, 5]
    with pytest.raises(Exception, match="Не удалось создать файл с результатом"):
        segment_replace(input_array, 1, 2, 6, 7)


def test_segment_replace_intersecting_segments():
    input_array = [1, 2, 3, 4, 5, 6]
    with pytest.raises(Exception, match="Не удалось создать файл с результатом"):
        segment_replace(input_array, 2, 4, 3, 5)


@pytest.mark.parametrize("array, a1, b1, a2, b2, expected", [
    ([1, 2, 3, 4, 5, 6], 1, 2, 5, 6, [5, 6, 3, 4, 1, 2]),
    ([10, 20, 30, 40, 50, 60], 2, 3, 4, 5, [10, 40, 50, 20, 30, 60]),
    ([7, 8, 9, 10, 11, 12], 1, 3, 4, 6, [10, 11, 12, 7, 8, 9])
])
def test_segment_replace_parametrized(array, a1, b1, a2, b2, expected):
    result = segment_replace(array, a1, b1, a2, b2)
    assert result == expected, f"Ошибка с параметрами {a1, b1, a2, b2}"


def test_main_function_call_with_mock(capsys):
    with patch("sys.argv", ["sgrpl", "1 2 3 4 5", [1, 2], [4, 5]]):
        main(["1 2 3 4 5", [1, 2], [4, 5]])
        captured = capsys.readouterr()
        assert "Массив после перестановки сегментов: [4, 5, 3, 1, 2]\n" in captured
