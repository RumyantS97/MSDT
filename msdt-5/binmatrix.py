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
        self.row_count = len(self.matrix)  # row number
        self.col_count = len(self.matrix[0])  # column number

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
        return [
            (1 << (self.row_count + self.col_count - 1 - i)) ^ matrix_int[i]
            for i in range(self.row_count)
        ]

    def __choose_element(self, row, col, matrix_int):
        """
        Choose a non-zero row started from position [row][col].
        """
        assert row <= col, (
            "The row index cannot exceed the column index "
            "in row-reduced echelon matrix."
        )

        if col == self.col_count:
            return None
        else:
            mask = (1 << (self.col_count - 1 - col))
            temp = [(matrix_int[i] & mask) for i in range(row,
                                                          self.row_count)]
            if mask not in temp:
                return self.__choose_element(row, col + 1, matrix_int)
            else:
                return (temp.index(mask) + row, col)

    @staticmethod
    def __switch_rows(row1, row2, matrix_int):
        """
        Switch row1-th and row2-th rows of matrix_int.
        """
        matrix_int[row1], matrix_int[row2] = matrix_int[
            row2
        ], matrix_int[row1]

    def __add_rows(self, row, col, matrix_int):
        """
        Add the row-th row to all the other rows if the col-th element of
        the corresponding rows are nonzero.
        """
        mask = (1 << (self.col_count - 1 - col))
        for i in range(self.row_count):
            if i != row and matrix_int[i] & mask != 0:
                matrix_int[i] ^= matrix_int[row]

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
        if [len(row) for row in self.matrix].count(
            self.row_count
        ) != self.row_count:
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
        Calculate the Rank of the matrix.
        """
        self.__is_matrix()
        self.__is_binary()
        matrix_int = self.__convert_matrix_to_int()
        row = 0
        col = 0
        for _ in range(self.row_count):
            arg = self.__choose_element(row, col, matrix_int)
            if arg is not None:
                row_temp, col = arg
                self.__switch_rows(row, row_temp, matrix_int)
                self.__add_rows(row, col, matrix_int)
                row += 1
                col += 1
            else:
                return row
        return self.row_count

    def det(self):
        """
        Calculate the determinant of the matrix.
        """
        self.__is_square_matrix()
        self.__is_binary()
        if self.rank() == self.row_count:
            return 1
        else:
            return 0

    def inv(self):
        """
        Calculate the inverse of the matrix.
        """
        self.__is_square_matrix()
        self.__is_binary()
        matrix_adj = self.__append_unit_matrix()
        row = 0
        col = 0
        for _ in range(self.row_count):
            arg = self.__choose_element(row, col, matrix_adj)
            if arg is not None:
                row_temp, col = arg
                self.__switch_rows(row, row_temp, matrix_adj)
                self.__add_rows(row, col, matrix_adj)
                row += 1
                col += 1
            else:
                raise RankError(row)
        return [
            [int(bit) for bit in format((matrix_adj[i] >> self.col_count),
                                        "0" + str(self.row_count) + "b")]
            for i in range(self.row_count)
        ]
