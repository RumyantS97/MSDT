import random


# Функция для создания матрицы заданного размера с случайными числами
def create_random_matrix(rows, cols):
    return [[random.randint(1, 10) for _ in range(cols)] for _ in range(rows)]


# Функция для отображения матрицы
def print_matrix(matrix, name):
    print(f"\nМатрица {name}:")
    for row in matrix:
        print(row)


# Функция для сложения двух матриц
def add_matrices(matrix_a, matrix_b):
    rows = len(matrix_a)
    cols = len(matrix_a[0])
    result_matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            result_matrix[i][j] = matrix_a[i][j] + matrix_b[i][j]
    return result_matrix


# Функция для вычитания двух матриц
def subtract_matrices(matrix_a, matrix_b):
    rows = len(matrix_a)
    cols = len(matrix_a[0])
    result_matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            result_matrix[i][j] = matrix_a[i][j] - matrix_b[i][j]
    return result_matrix


# Функция для умножения двух матриц
def multiply_matrices(matrix_a, matrix_b):
    rows_a = len(matrix_a)
    cols_a = len(matrix_a[0])
    cols_b = len(matrix_b[0])
    result_matrix = [[0 for _ in range(cols_b)] for _ in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result_matrix[i][j] += matrix_a[i][k]*matrix_b[k][j]
    return result_matrix


# Функция для транспонирования матрицы
def transpose_matrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    transposed_matrix = [[0 for _ in range(rows)] for _ in range(cols)]
    for i in range(rows):
        for j in range(cols):
            transposed_matrix[j][i] = matrix[i][j]
    return transposed_matrix


# Функция для вычисления определителя 2x2 матрицы
def determinant2x2(matrix):
    return (matrix[0][0] * matrix[1][1] -
            matrix[0][1] * matrix[1][0])


# Функция для вычисления определителя 3x3 матрицы
def determinant3x3(matrix):
    det = (matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]) -
           matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0]) +
           matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]))
    return det


# Функция для вычисления следа матрицы
def trace_matrix(matrix):
    trace = 0
    size = min(len(matrix), len(matrix[0]))
    for i in range(size):
        trace += matrix[i][i]
    return trace


# Функция для скалярного умножения матрицы на число
def scalar_multiply(matrix, scalar):
    rows = len(matrix)
    cols = len(matrix[0])
    result_matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            result_matrix[i][j] = matrix[i][j] * scalar
    return result_matrix


# Функция для нахождения максимального элемента в матрице
def max_element(matrix):
    max_val = matrix[0][0]
    for row in matrix:
        for value in row:
            if value > max_val:
                max_val = value
    return max_val


# Функция для нахождения минимального элемента в матрице
def min_element(matrix):
    min_val = matrix[0][0]
    for row in matrix:
        for value in row:
            if value < min_val:
                min_val = value
    return min_val


# Функция для проверки, является ли матрица симметричной
def is_symmetric(matrix):
    rows = len(matrix)
    for i in range(rows):
        for j in range(i + 1, rows):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True


# Функция для сравнения двух матриц на равенство
def matrices_equal(matrix_a, matrix_b):
    if len(matrix_a) != len(matrix_b) or len(matrix_a[0]) != len(matrix_b[0]):
        return False
    for i in range(len(matrix_a)):
        for j in range(len(matrix_a[0])):
            if matrix_a[i][j] != matrix_b[i][j]:
                return False
    return True


# Функция для сложения всех элементов матрицы
def sum_of_elements(matrix):
    total_sum = 0
    for row in matrix:
        total_sum += sum(row)
    return total_sum


# Функция для создания единичной матрицы заданного размера
def identity_matrix(size):
    identity_mat = [[1 if i == j else 0
                     for j in range(size)]
                    for i in range(size)]

    return identity_mat


# Функция для нахождения максимального значения в каждом столбце
def max_in_columns(matrix):
    num_cols = len(matrix[0])
    max_values = []
    for j in range(num_cols):
        col_max = float('-inf')
        for i in range(len(matrix)):
            if matrix[i][j] > col_max:
                col_max = matrix[i][j]
        max_values.append(col_max)
    return max_values


# Функция для нахождения минимального значения в каждом столбце
def min_in_columns(matrix):
    num_cols = len(matrix[0])
    min_values = []
    for j in range(num_cols):
        col_min = float('inf')
        for i in range(len(matrix)):
            if matrix[i][j] < col_min:
                col_min = matrix[i][j]
        min_values.append(col_min)
    return min_values


# Функция для создания нулевой матрицы заданного размера
def zero_matrix(rows, cols):
    return [[0] * cols for _ in range(rows)]


# Функция для сложения всех элементов матрицы
def sum_of_elements(matrix):
    total_sum = 0
    for row in matrix:
        total_sum += sum(row)
    return total_sum


# Функция для проверки, является ли матрица диагональной
def is_diagonal(matrix):
    rows = len(matrix)
    for i in range(rows):
        for j in range(len(matrix[i])):
            if i != j and matrix[i][j] != 0:
                return False
    return True


# Функция для нахождения подматрицы (удаление заданной строки и столбца)
def submatrix(matrix, remove_row, remove_col):
    sub_mat = []
    for i in range(len(matrix)):
        if i == remove_row:
            continue
        new_row = []
        for j in range(len(matrix[i])):
            if j == remove_col:
                continue
            new_row.append(matrix[i][j])
        sub_mat.append(new_row)
    return sub_mat


# Ввод размеров матриц от пользователя
rows = int(input("Введите количество строк: "))
cols = int(input("Введите количество столбцов: "))

# Создаем две случайные матрицы
matrix_A = create_random_matrix(rows, cols)
matrix_B = create_random_matrix(rows, cols)

# Выводим созданные матрицы
print_matrix(matrix_A, 'A')
print_matrix(matrix_B, 'B')

# Сложение матриц
matrix_C = add_matrices(matrix_A, matrix_B)
print_matrix(matrix_C, 'C (A + B)')

# Вычитание матриц
matrix_D = subtract_matrices(matrix_A, matrix_B)
print_matrix(matrix_D, 'D (A - B)')

# Умножение матриц (только если количество столбцов A равно количеству строк B)
if cols == rows:
    matrix_E = multiply_matrices(matrix_A, matrix_B)
    print_matrix(matrix_E, 'E (A * B)')

    # Вычисление определителя 3x3 матрицы (если размерность 3x3)
    if rows == 3 and cols == 3:
        det_A = determinant3x3(matrix_A)
        det_B = determinant3x3(matrix_B)
        print(f"\nОпределитель матрицы A: {det_A}")
        print(f"Определитель матрицы B: {det_B}")

    # Вычисление следа матриц
    trace_A = trace_matrix(matrix_A)
    trace_B = trace_matrix(matrix_B)
    print(f"\nСлед матрицы A: {trace_A}")
    print(f"След матрицы B: {trace_B}")

    # Транспонирование матрицы A
    transposed_F_A = transpose_matrix(matrix_A)
    print_matrix(transposed_F_A, 'F (A^T)')

    # Транспонирование матрицы B
    transposed_G_B = transpose_matrix(matrix_B)
    print_matrix(transposed_G_B, 'G (B^T)')

    # Скалярное умножение на число (например, 2)
    scalar_value = 2
    scaled_H_A = scalar_multiply(matrix_A, scalar_value)
    print_matrix(scaled_H_A, f'H (A * {scalar_value})')

# Нахождение максимального и минимального элементов в матрице А
max_A_element = max_element(matrix_A)
min_A_element = min_element(matrix_A)

# Нахождение максимального и минимального элементов в матрице B
max_B_element = max_element(matrix_B)
min_B_element = min_element(matrix_B)

print(f"\nМаксимальный элемент в A: {max_A_element}")
print(f"Минимальный элемент в A: {min_A_element}")

print(f"Максимальный элемент в B: {max_B_element}")
print(f"Минимальный элемент в B: {min_B_element}")

# Проверка на симметричность
symmetrical_A_flag = is_symmetric(matrix_A)
symmetrical_B_flag = is_symmetric(matrix_B)

print(f"\nМатрица A симметрична: {symmetrical_A_flag}")
print(f"Матрица B симметрична: {symmetrical_B_flag}")

# Сравнение двух матриц на равенство
equal_check_flag = matrices_equal(matrix_A, matrix_B)
print(f"\nМатрица A равна Матрице B: {equal_check_flag}")

# Сложение всех элементов в A и B
total_sum_A = sum_of_elements(matrix_A)
total_sum_B = sum_of_elements(matrix_B)

print(f"\nСумма всех элементов в A: {total_sum_A}")
print(f"Сумма всех элементов в B: {total_sum_B}")

# Создание единичной матрицы
identity_mat_size = min(rows, cols)
identity_mat = identity_matrix(identity_mat_size)
print_matrix(identity_mat, "Eдиничная Матрица")

# Проверка на диагональность
diag_A = is_diagonal(matrix_A)
diag_B = is_diagonal(matrix_B)

print(f"\nМатрица A диагональная: {diag_A}")
print(f"Матрица B диагональная: {diag_B}")

# Максимальные значения в каждом слолбце для А и B
max_in_cols_A = max_in_columns(identity_mat)
max_in_cols_B = max_in_columns(identity_mat)

print(f"\nМаксимальные значения в каждом столбце для A: {max_in_cols_A}")
print(f"Максимальные значения в каждом столбце для B: {max_in_cols_B}")

# Минимальные значения в каждом слолбце для А и B
min_in_cols_A = min_in_columns(identity_mat)
min_in_cols_B = min_in_columns(identity_mat)

print(f"\nМинимальные значения в каждом столбце для A: {min_in_cols_A}")
print(f"Минимальные значения в каждом столбце для B: {min_in_cols_B}")

# Построение нулевой матрицы
zero_mat = zero_matrix(rows, cols)
print_matrix(zero_mat, "Нулевая Матрица")

# Нахождение подматрицы после удаления первой строки и первого столбца
sub_mat = submatrix(matrix_A, 0, 0)

print_matrix(sub_mat, "Подматрица после удаления первой строки и первого столбца")

# Вывод сообщения о завершении работы программы
print("\nВсе операции выполнены успешно!")
