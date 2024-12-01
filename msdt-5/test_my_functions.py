import pytest
from pytest_mock import MockerFixture
from my_functions import find_longest_increasing_subsequence, check_parentheses, check_all_brackets, zero_matrix


def test_longest_increasing_subsequence_single_element():
    assert find_longest_increasing_subsequence([5]) == [5]


def test_longest_increasing_subsequence_single_two_elements_increasing():
    assert find_longest_increasing_subsequence([1, 2]) == [1, 2]


def test_longest_increasing_subsequence_single_multiple_elements_increasing():
    assert find_longest_increasing_subsequence([1, 2, 3, 4]) == [1, 2, 3, 4]


def test_longest_increasing_subsequence_single_mixed_elements():
    assert find_longest_increasing_subsequence([5, 3, 4, 8, 6, 7]) == [3, 4, 6, 7]


def test_longest_increasing_subsequence_single_repeated_elements():
    assert find_longest_increasing_subsequence([1, 2, 2, 3]) == [1, 2, 3]


def test_longest_increasing_subsequence_single_multiple_elements_decreasing():
    assert find_longest_increasing_subsequence([5, 4, 3, 2, 1]) == [5]


def test_longest_increasing_subsequence_single_two_elements_decreasing():
    assert find_longest_increasing_subsequence([-2, 2, 1]) == [-2, 2]


def test_longest_increasing_subsequence_single_large_sequence():
    # Generate random sequence of 1000 elements
    sequence = list(range(1000))
    import random
    random.shuffle(sequence)
    result = find_longest_increasing_subsequence(sequence)
    assert len(result) <= 1000
    # Check that the subsequence is indeed increasing
    assert all(result[i] < result[i + 1] for i in range(len(result) - 1))


def test_longest_increasing_subsequence_single_invalid_type():
    with pytest.raises(ValueError):
        find_longest_increasing_subsequence(['a', 'b', 'c'])


def test_longest_increasing_subsequence_single_non_integer_input():
    with pytest.raises(ValueError):
        find_longest_increasing_subsequence([1.1, 2.2, 3.4, 4.5])


def test_longest_increasing_subsequence_single_empty_input():
    with pytest.raises(TypeError):
        find_longest_increasing_subsequence([])


def test_check_parentheses_empty():
    assert check_parentheses("") == True


def test_check_parentheses_correct():
    assert check_parentheses("()") == True
    assert check_parentheses("((()))") == True
    assert check_parentheses("(()())") == True


def test_check_parentheses_incorrect():
    assert check_parentheses("(") == False
    assert check_parentheses(")") == False
    assert check_parentheses("())") == False
    assert check_parentheses("(()") == False
    assert check_parentheses(")(()") == False

    
# Parameterized test for check_all_brackets (more efficient than many individual tests)
@pytest.mark.parametrize("input_string, expected", 
                         [("()", True),
                          ("(){}[]", True),
                          ("{[()]}", True),
                          ("([{}])", True),
                          ("((()))", True),
                          (")(", False),
                          ("({[})]", False),
                          ("{[(])}", False),
                          ("(()", False),
                          ("", True), #empty case
                          ("[(])", False),
                          ("{[", False), ])
def test_check_all_brackets_parametrized(input_string, expected):
    assert check_all_brackets(input_string) == expected
    
    
def test_zero_matrix_empty():
    assert zero_matrix([[]]) == [[]]


def test_zero_matrix_no_zeros():
    matrix = [[1, 2], [3, 4]]
    assert zero_matrix(matrix.copy()) == [[1, 2], [3, 4]]


def test_zero_matrix_one_zero():
    matrix = [[1, 0], [3, 4]]
    assert zero_matrix(matrix.copy()) == [[0, 0], [3, 0]]
    

# Test for irregular matrix (raises IndexError)
def test_zero_matrix_irregular_matrix():
    with pytest.raises(IndexError):
        zero_matrix([[1, 2], [3, 4, 5]])


# Parameterized test for zero_matrix (more efficient than many individual tests)
@pytest.mark.parametrize("matrix, expected",
                         [([[1, 0], [0, 1]], [[0, 0], [0, 0]]),          
                          ([[0, 1], [1, 0]], [[0, 0], [0, 0]]),          
                          ([[1, 1], [1, 1]], [[1, 1], [1, 1]]),          
                          ([[1, 0, 1], [0, 1, 0]], [[0, 0, 0], [0, 0, 0]]), 
                          ([[0, 0], [0, 0]], [[0, 0], [0, 0]]),          
                          ([ [1] ], [[1]]),                               
                          ([], []), ])
def test_zero_matrix_parametrized(matrix, expected):
    original_matrix = [row[:] for row in matrix]
    result = zero_matrix(matrix) 
    assert result == expected
    assert matrix == original_matrix  


# Mocking test (check for side effects)
def test_zero_matrix_no_side_effects(mocker: MockerFixture):
    mock_print = mocker.patch('builtins.print')  # Mock the print function
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    zero_matrix(matrix)
    mock_print.assert_not_called()  # Assert that print wasn't called