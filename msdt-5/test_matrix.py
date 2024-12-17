import pytest
from unittest.mock import patch
from binmatrix import BinMatrix, DataError, FormatError, RankError


valid_matrix = [[1, 0, 1], [0, 1, 1], [1, 1, 0]]
non_binary_matrix = [[1, 0, 2], [0, 1, 1], [1, 1, 0]]
non_square_matrix = [[1, 0, 1], [0, 1, 1]]
rank_deficient_matrix = [[1, 1, 0], [1, 1, 0], [0, 0, 0]]
square_full_rank_matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]


@pytest.mark.parametrize("matrix, expected_rank", [
    (valid_matrix, 2),
    (rank_deficient_matrix, 1)
])
def test_rank(matrix, expected_rank):
    bm = BinMatrix(matrix)
    assert bm.rank() == expected_rank


@pytest.mark.parametrize("matrix, expected_det", [
    (square_full_rank_matrix, 1),
    (rank_deficient_matrix, 0)
])
def test_det(matrix, expected_det):
    bm = BinMatrix(matrix)
    assert bm.det() == expected_det


def test_non_binary_elements():
    with pytest.raises(DataError) as exc_info:
        bm = BinMatrix(non_binary_matrix)
        bm.__is_binary()
    assert exc_info.type == DataError
    exc_info.value.print_error()


def test_non_square_matrix():
    with pytest.raises(FormatError) as exc_info:
        bm = BinMatrix(non_square_matrix)
        bm.det()
    assert exc_info.type == FormatError
    exc_info.value.print_error()


def test_inverse_matrix():
    bm = BinMatrix(square_full_rank_matrix)
    inv_matrix = bm.inv()
    expected_inverse = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]
    assert inv_matrix == expected_inverse


def test_rank_error_on_inverse():
    with pytest.raises(RankError) as exc_info:
        bm = BinMatrix(rank_deficient_matrix)
        bm.inv()
    assert exc_info.type == RankError
    exc_info.value.print_error()


@patch.object(BinMatrix, '_BinMatrix__convert_matrix_to_int', return_value=[0b101, 0b011, 0b110])
def test_mock_convert_matrix_to_int(mock_method):
    bm = BinMatrix(valid_matrix)
    result = bm._BinMatrix__convert_matrix_to_int()
    assert result == [0b101, 0b011, 0b110]
    mock_method.assert_called_once()
