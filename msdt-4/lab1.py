import numpy as np
from itertools import combinations
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Генерация случайной размерности матрицы
rows = np.random.randint(5, 11)  # случайное количество строк от 5 до 10
cols = np.random.randint(5, 11)  # случайное количество столбцов от 5 до 10
logger.info(f"Сгенерированы размеры матрицы: {rows}x{cols}")

# Генерация матрицы, состоящей из нулей и единиц
matrix = np.random.randint(0, 2, size=(rows, cols))
logger.info(f"Сгенерирована матрица: \n{matrix}")

# Матрица из примера
example_G = np.array([[1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1],
                      [0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0],
                      [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]])
logger.info(f"Матрица из примера: \n{example_G}")


def REF(matrix):
    logger.info("Начало вычисления матрицы ступенчатого вида (REF)")
    mat = matrix.astype(int)
    rows, cols = mat.shape
    lead_col = 0

    for row in range(rows):
        if lead_col >= cols:
            return mat

        i = row
        while mat[i, lead_col] == 0:
            i += 1
            if i == rows:
                i = row
                lead_col += 1
                if lead_col == cols:
                    return mat

        mat[[i, row]] = mat[[row, i]]

        for i in range(row + 1, rows):
            if mat[i, lead_col] == 1:
                mat[i] = (mat[i] + mat[row]) % 2

        lead_col += 1

    logger.info("Вычисление REF завершено")
    return mat


ref = REF(example_G)
logger.info(f"Матрица ступенчатого вида: \n{ref}")


def RREF(matrix):
    logger.info(
        "Начало вычисления приведенной матрицы ступенчатого вида (RREF)")
    mat = matrix.astype(int)
    rows, cols = mat.shape
    lead_col = 0

    for row in range(rows):
        if lead_col >= cols:
            return mat

        i = row
        while mat[i, lead_col] == 0:
            i += 1
            if i == rows:
                i = row
                lead_col += 1
                if lead_col == cols:
                    return mat

        mat[[i, row]] = mat[[row, i]]

        for i in range(rows):
            if i != row and mat[i, lead_col] == 1:
                mat[i] = (mat[i] + mat[row]) % 2

        lead_col += 1

    logger.info("Вычисление RREF завершено")
    return mat


rref = RREF(example_G)
logger.info(f"Приведенная матрица ступенчатого вида: \n{rref}")


def fix_lead_cols(matrix):
    logger.info("Определение ведущих столбцов")
    rows, cols = matrix.shape
    lead_cols = []

    for row in range(rows):
        for col in range(cols):
            if matrix[row, col] == 1:
                lead_cols.append(col)
                break

    logger.info(f"Ведущие столбцы: {lead_cols}")
    return lead_cols


lead_cols = fix_lead_cols(rref)


def delete_lead_cols(matrix, lead_cols):
    logger.info("Удаление ведущих столбцов")
    return np.delete(matrix, lead_cols, axis=1)


X = delete_lead_cols(rref, lead_cols)
logger.info(f"Сокращённая матрица: \n{X}")

I = np.eye(len(X[0]), dtype=int)
logger.info(f"Единичная матрица: \n{I}")


def H_matrix_create(X, lead_cols, I):
    logger.info("Создание матрицы H")
    cols = np.shape(X)[1]
    rows = np.shape(X)[0] + np.shape(I)[0]
    strX = 0
    strI = 0
    H = np.zeros((rows, cols), dtype=int)
    for i in range(rows):
        if i in lead_cols:
            H[i, :] = X[strX, :]
            strX += 1
        else:
            H[i, :] = I[strI, :]
            strI += 1

    logger.info(f"Матрица H создана: \n{H}")
    return H


H = H_matrix_create(X, lead_cols, I)


def codewords_by_sum(example_G, k):
    logger.info("Генерация кодовых слов способом суммы")
    codewords = set()

    for r in range(1, k + 1):
        for comb in combinations(range(k), r):
            codeword = np.bitwise_xor.reduce(example_G[list(comb)], axis=0)
            codewords.add(tuple(codeword))

    codewords.add(tuple(np.zeros(example_G.shape[1], dtype=int)))
    logger.info("Кодовые слова сгенерированы")
    return np.array(list(codewords))


sum_codewords = codewords_by_sum(example_G, example_G.shape[0])


def codewords_by_multiplication(G, k):
    logger.info("Генерация кодовых слов способом умножения")
    codewords = []

    for i in range(2 ** k):
        binary_word = np.array(list(np.binary_repr(i, k)), dtype=int)
        codeword = np.dot(binary_word, G) % 2
        codewords.append(codeword)

    logger.info("Кодовые слова сгенерированы")
    return np.array(codewords)


mult_codewords = codewords_by_multiplication(example_G, example_G.shape[0])
logger.info(f"Кодовые слова совпадают: {set(map(tuple, sum_codewords))
                                        == set(map(tuple, mult_codewords))}")


def distance(sum_codewords):
    logger.info("Вычисление кодового расстояния")
    min_weight = float('inf')
    for word in sum_codewords:
        weight = np.sum(word)
        if 0 < weight < min_weight:
            min_weight = weight
    logger.info(f"Кодовое расстояние: {min_weight}")
    return min_weight


logger.info(f"Кодовое расстояние: {distance(sum_codewords)}")

error = np.zeros_like(sum_codewords[0])
error[4] = 1
codeword_with_error = error + sum_codewords[22]
xor_error_codeword = codeword_with_error % 2


def check(codeword, H):
    logger.info("Проверка кодового слова на наличие ошибок")
    return np.dot(codeword, H) % 2


logger.info(f"Обнаружение ошибки: {check(xor_error_codeword, H)}")

error_2 = np.zeros_like(sum_codewords[0])
error_2[6] = 1
error_2[9] = 1
codeword_with_error_2 = error_2 + sum_codewords[22]
xor_error_codeword_2 = codeword_with_error_2 % 2

logger.info(f"Отсутствие ошибки: {check(xor_error_codeword_2, H)}")
