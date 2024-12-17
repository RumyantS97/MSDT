from functools import reduce

# For feedback or questions, please contact at xiangzejun@iie.ac.cn
# Implemented by Xiang Zejun, State Key Laboratory of Information Security,
# Institute Of Information Engineering, CAS


class DataError(Exception):
    """
    Define my data exception.
    Check whether the elements of the matrix are binaries.
    """

    def __init__(self, row, col):
        """
        Store the coordinate of the entry which is not binary.
        """
        self.row = row
        self.col = col

    def print_error(self):
        print("The element at [{0}][{1}] is NOT binary!".format(
            self.row, self.col))


class FormatError(Exception):
    """
    Define my format exception.
    Check whether input is a matrix or a square matrix.
    """

    def __init__(self, message):
        self.error = "The input is " + message

    def print_error(self):
        print(self.error)


class RankError(Exception):
    """
    Define my rank exception.
    Check whether the square matrix is full rank when calculating its inverse.
    """

    def __init__(self, rank):
        self.rank = rank

    def print_error(self):
        print("The matrix is NOT full rank. (rank = {0})".format(self.rank))


class BinMatrix:
    def __init__(self, matrix=None):
        """
        Initialize a matrix.
        """
        if matrix is None:
            matrix = [[1]]
        self.matrix = matrix
        self.row_count = len(self.matrix)
        self.col_count = len(self.matrix[0])
        self.__is_matrix()
        self.__is_binary()

    def __convert_matrix_to_int(self):
        """
        Convert each row of the binary matrix to an integer.
        """
        return [
            int("".join(map(str, self.matrix[i])), 2)
            for i in range(self.row_count)
        ]

    def __append_unit_matrix(self):
        """
        Append a unit matrix to matrix_int.
        """
        matrix_int = self.__convert_matrix_to_int()
        for i in range(self.row_count):
            matrix_int[i] <<= self.row_count
            matrix_int[i] |= (1 << (self.row_count - 1 - i))
        return matrix_int

    def __choose_pivot_row(self, col, matrix_int, start_row):
        """
        Choose the row with a non-zero pivot in the given column.
        """
        for row in range(start_row, self.row_count):
            if matrix_int[row] & (1 << (self.col_count - 1 - col)):
                return row
        return None

    def __switch_rows(self, row1, row2, matrix_int):
        """
        Switch row1-th and row2-th rows of matrix_int.
        """
        matrix_int[row1], matrix_int[row2] = matrix_int[
            row2
        ], matrix_int[row1]

    def __eliminate_rows(self, pivot_row, col, matrix_int):
        """
        Eliminate the given column in all rows except the pivot row.
        """
        for row in range(self.row_count):
            if row != pivot_row and matrix_int[
                row
            ] & (1 << (self.col_count - 1 - col)):
                matrix_int[row] ^= matrix_int[pivot_row]

    def __is_matrix(self):
        """
        Check whether the input is a matrix.
        """
        if [len(row) for row in self.matrix].count(
            self.col_count
        ) != self.row_count:
            raise FormatError("NOT a matrix!")

    def __is_square_matrix(self):
        """
        Check whether the input is a square matrix.
        """
        if self.row_count != self.col_count:
            raise FormatError("NOT a Square matrix!")

    def __is_binary(self):
        """
        Check whether the entries in the input are binaries.
        """
        for row_index in range(len(self.matrix)):
            for col_index in range(len(self.matrix[row_index])):
                if self.matrix[row_index][col_index] not in [0, 1]:
                    raise DataError(row_index, col_index)

    def rank(self):
        """
        Calculate the rank of the matrix.
        """
        matrix_int = self.__convert_matrix_to_int()
        rank = 0
        for col in range(self.col_count):
            pivot_row = self.__choose_pivot_row(col, matrix_int, rank)
            if pivot_row is not None:
                self.__switch_rows(rank, pivot_row, matrix_int)
                self.__eliminate_rows(rank, col, matrix_int)
                rank += 1
        return rank

    def det(self):
        """
        Calculate the determinant of the matrix.
        """
        self.__is_square_matrix()
        return 1 if self.rank() == self.row_count else 0

    def inv(self):
        """
        Calculate the inverse of the binary square
        matrix using Gaussian elimination modulo 2.
        """
        self.__is_square_matrix()
        if self.rank() < self.row_count:
            raise RankError(self.rank())

        matrix_adj = self.__append_unit_matrix()
        for col in range(self.col_count):
            pivot_row = self.__choose_pivot_row(col, matrix_adj, col)
            if pivot_row is None:
                raise RankError(col)

            self.__switch_rows(col, pivot_row, matrix_adj)
            self.__eliminate_rows(col, col, matrix_adj)

        inverse = []
        for row in range(self.row_count):
            row_bits = matrix_adj[row] >> self.row_count
            inverse.append([
                int(bit) for bit in format(row_bits, f"0{self.row_count}b")
            ])
        return inverse
