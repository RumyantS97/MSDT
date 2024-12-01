import sys

def find_longest_increasing_subsequence(sequence):
    """
    Finds the longest increasing subsequence in a given sequence of integers.

    :param sequence: A list of integers.

    :return: A list representing the longest increasing subsequence.

    :raises: ValueError: If the input sequence contains non-integer values.
             TypeError: If the input sequence is empty.
    """
    if not all(isinstance(x, int) for x in sequence):
        raise ValueError("Input sequence must contain only integers.")
    if not sequence:
        raise TypeError("Input sequence must contain at least one element.")

    n = len(sequence)
    dp = [1] * n  # dp[i] stores the length of the LIS ending at index i
    prev_index = [-1] * n  # prev_index[i] stores the index of the previous element in the LIS ending at index i

    for i in range(1, n):
        for j in range(i):
            if sequence[i] > sequence[j] and dp[i] < dp[j] + 1:
                dp[i] = dp[j] + 1
                prev_index[i] = j

    max_length = max(dp)
    index = dp.index(max_length)

    lis = []
    while index != -1:
        lis.append(sequence[index])
        index = prev_index[index]

    return lis[::-1]


def check_parentheses(string):
    """
    Checks if parentheses are correctly balanced in a string.

    :param string: The input string containing parentheses.

    :return: True if parentheses are balanced, False otherwise.
    """
    counter = 0
    for char in string:
        if char == '(':
            counter += 1
        elif char == ')':
            if counter == 0:
                return False
            counter -= 1
    return counter == 0


def check_all_brackets(string):
    """
    Checks if all brackets ((), {}, []) are correctly balanced in a string.

    :param string: The input string containing brackets.

    :return: True if brackets are balanced, False otherwise.
    """
    stack = []
    bracket_map = {')': '(', '}': '{', ']': '['}
    for char in string:
        if char in ['(', '{', '[']:
            stack.append(char)
        elif char in [')', '}', ']']:
            if not stack or stack.pop() != bracket_map[char]:
                return False
    return not stack


def zero_matrix(matrix):
    """
    Zeros out the row and column of any zero element in a matrix.

    :param matrix: A list of lists representing the matrix.

    :return: A *new* matrix with zeroed rows and columns.  The original matrix is unchanged.

    :raises: IndexError: If the input matrix is irregular (rows have different lengths).
    """
    if not matrix:
        return []

    rows = len(matrix)
    cols = len(matrix[0])

    # Check for matrix irregularity
    if any(len(row) != cols for row in matrix):
        raise IndexError("Irregular matrix: Rows must have the same length.")

    # Create a copy of the matrix
    new_matrix = [row[:] for row in matrix]

    rows_with_zeros = [False] * rows
    cols_with_zeros = [False] * cols

    # Find rows and columns with zeros
    for i in range(rows):
        for j in range(cols):
            if new_matrix[i][j] == 0:
                rows_with_zeros[i] = True
                cols_with_zeros[j] = True

    # Reset rows and columns in the copy
    for i in range(rows):
        if rows_with_zeros[i]:
            new_matrix[i] = [0] * cols

    for j in range(cols):
        if cols_with_zeros[j]:
            for i in range(rows):
                new_matrix[i][j] = 0

    return new_matrix


def main():
    """
    Main function to handle command-line arguments and print the longest increasing subsequence.
    """
    if len(sys.argv) < 2:
        print("Invalid number of sequence elements. Please enter at least one integer.")
        return

    sequence = []
    for arg in sys.argv[1:]:
        try:
            num = int(arg)
            sequence.append(num)
        except ValueError:
            print(f"Invalid input: '{arg}'. Please enter only integers.")
            return

    lis = find_longest_increasing_subsequence(sequence)
    print(f"Longest increasing subsequence: {lis}")

if __name__ == "__main__":
    main()
