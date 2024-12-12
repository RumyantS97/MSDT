def print_matrix(matrix):
    """Output of the matrix in a convenient way."""
    for row in matrix:
        print(" ".join(map(str, row)))
    print()


def add_matrices(matrix1, matrix2):
    """The addition of two matrices."""
    if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
        raise ValueError("The matrices must be the same size for addition.")
    return [
        [matrix1[i][j] + matrix2[i][j] for j in range(len(matrix1[0]))]
        for i in range(len(matrix1))
    ]


def subtract_matrices(matrix1, matrix2):
    """Subtraction of one matrix from another."""
    if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
        raise ValueError("The matrices must be the same size for subtraction.")
    return [
        [matrix1[i][j] - matrix2[i][j] for j in range(len(matrix1[0]))]
        for i in range(len(matrix1))
    ]


def transpose_matrix(matrix):
    """Matrix transposition."""
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]


def multiply_matrices(matrix1, matrix2):
    """Multiplication of two matrices."""
    if len(matrix1[0]) != len(matrix2):
        raise ValueError(
            "The number of columns of the first matrix must be equal to the number of rows of the second one.")
    return [
        [sum(matrix1[i][k] * matrix2[k][j] for k in range(len(matrix2)))
         for j in range(len(matrix2[0]))]
        for i in range(len(matrix1))
    ]


def is_square_matrix(matrix):
    """Checks whether the matrix is square."""
    return len(matrix) == len(matrix[0])


def scalar_multiply_matrix(matrix, scalar):
    """Multiplication of a matrix by a scalar."""
    return [[scalar * element for element in row] for row in matrix]


def trace_matrix(matrix):
    """Calculating the footprint of a square matrix (the sum of the elements on the main diagonal)."""
    if not is_square_matrix(matrix):
        raise ValueError(
            "The trace can only be calculated for a square matrix.")
    return sum(matrix[i][i] for i in range(len(matrix)))


def determinant_matrix(matrix):
    """Recursive calculation of the determinant of a square matrix."""
    if not is_square_matrix(matrix):
        raise ValueError(
            "The determinant can only be calculated for a square matrix.")
    if len(matrix) == 1:
        return matrix[0][0]
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    determinant = 0
    for col in range(len(matrix)):
        minor = [[row[i] for i in range(len(row)) if i != col]
                 for row in matrix[1:]]
        determinant += ((-1) ** col) * \
            matrix[0][col] * determinant_matrix(minor)
    return determinant


def identity_matrix(size):
    """Creates a single matrix of a given size."""
    return [[1 if i == j else 0 for j in range(size)] for i in range(size)]


def inverse_matrix(matrix):
    """Calculates the inverse matrix (for a non-degenerate square matrix)."""
    if not is_square_matrix(matrix):
        raise ValueError("The inverse matrix exists only for a square matrix.")
    det = determinant_matrix(matrix)
    if det == 0:
        raise ValueError("The matrix is degenerate, there is no inverse.")

    size = len(matrix)
    adjugate = [[0] * size for _ in range(size)]

    for i in range(size):
        for j in range(size):
            minor = [[matrix[x][y] for y in range(size) if y != j]
                     for x in range(size) if x != i]
            adjugate[j][i] = ((-1) ** (i + j)) * determinant_matrix(minor)

    return scalar_multiply_matrix(adjugate, 1 / det)
