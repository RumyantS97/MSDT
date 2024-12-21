import pytest
from unittest.mock import mock_open, patch
from main import find_largest_number_less_or_equal, read_input_from_file, write_output_to_file

# Test for find_largest_number_less_or_equal
@pytest.mark.parametrize(
    "array, n, expected",
    [
        ([1, 2, 3, 4, 5], 3, 3),
        ([10, 20, 30, 40], 25, 20),
        ([5, 5, 5, 5], 5, 5),
        ([100, 200, 300], 50, None),
        ([1, 2, 3, 4], 0, None),
        ([-10, -20, -30, -40], -15, -20),
        ([], 10, None),
    ]
)
def test_find_largest_number_less_or_equal(array, n, expected):
    assert find_largest_number_less_or_equal(array, n) == expected

# Test for read_input_from_file
@patch("builtins.open", new_callable=mock_open, read_data="1 2 3 4\n10")
def test_read_input_from_file(mock_file):
    array, n = read_input_from_file("dummy_path.txt")
    assert array == [1, 2, 3, 4]
    assert n == 10

@patch("builtins.open", side_effect=FileNotFoundError)
def test_read_input_from_file_not_found(mock_file):
    with pytest.raises(FileNotFoundError):
        read_input_from_file("non_existent_file.txt")

# Test for write_output_to_file
@patch("builtins.open", new_callable=mock_open)
def test_write_output_to_file(mock_file):
    write_output_to_file("dummy_path.txt", 42)
    mock_file().write.assert_called_once_with("Наибольшее число <= n: 42")

@patch("builtins.open", new_callable=mock_open)
def test_write_output_to_file_none(mock_file):
    write_output_to_file("dummy_path.txt", None)
    mock_file().write.assert_called_once_with("Подходящее число не найдено.")

# Complex test with large data set
@pytest.mark.parametrize("array, n, expected", [
    (list(range(100000)), 99999, 99999),
    (list(range(-100000, 0)), -1, -1)
])
def test_large_data_sets(array, n, expected):
    assert find_largest_number_less_or_equal(array, n) == expected

# Mocking an exception during file writing
@patch("builtins.open", side_effect=OSError("File system error"))
def test_write_output_to_file_exception(mock_file):
    with pytest.raises(OSError):
        write_output_to_file("dummy_path.txt", 42)

if __name__ == "__main__":
    pytest.main()
