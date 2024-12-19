import random
import logging

from config import logging_config


logging_config()


def start_game():
    logging.info("Инициализация новой игры")
    mat = []
    for i in range(4):
        mat.append([0]*4)
    logging.info(f"Начальная матрица: {mat}")
    return mat


def add_new_2(mat):
    logging.info("Добавление новой двойки в матрицу")
    r = random.randint(0, 3)
    c = random.randint(0, 3)
    while (mat[r][c] != 0):
        r = random.randint(0, 3)
        c = random.randint(0, 3)
    mat[r][c] = 2
    logging.info(f"Добавлена двойка в позицию ({r}, {c})")


def reverse(mat):
    logging.info("Реверсирование строк матрицы")
    new_mat = []
    for i in range(4):
        new_mat.append([])
        for j in range(4):
            new_mat[i].append(mat[i][4-j-1])
    logging.info(f"Результат реверса: {new_mat}")
    return new_mat


def transpose(mat):
    logging.info("Транспонирование матрицы")
    new_mat = []
    for i in range(4):
        new_mat.append([])
        for j in range(4):
            new_mat[i].append(mat[j][i])
    logging.info(f"Результат транспонирования: {new_mat}")
    return new_mat


def merge(mat):
    logging.info("Слияние элементов в строках")
    changed = False
    for i in range(4):
        for j in range(3):
            if mat[i][j] == mat[i][j+1] and mat[i][j] != 0:
                mat[i][j] = mat[i][j]*2
                mat[i][j+1] = 0
                changed = True
                logging.info(f"Слиты элементы в строке {i} на позициях {j} и {j + 1}")
    return mat, changed


def compress(mat):
    logging.info("Сжатие элементов в строках матрицы")
    changed = False
    new_mat = []
    for i in range(4):
        new_mat.append([0]*4)

    for i in range(4):
        pos = 0
        for j in range(4):
            if mat[i][j] != 0:
                new_mat[i][pos] = mat[i][j]
                if j != pos:
                    changed = True
                pos += 1
    logging.info(f"Результат сжатия: {new_mat}")
    return new_mat, changed


def move_up(grid):
    logging.info("Движение вверх")
    transposed_grid = transpose(grid)
    new_grid, changed1 = compress(transposed_grid)
    new_grid, changed2 = merge(new_grid)
    changed = changed1 or changed2
    new_grid, temp = compress(new_grid)
    final_grid = transpose(new_grid)
    logging.info(f"Матрица после движения вверх: {final_grid}")
    return final_grid, changed


def move_down(grid):
    logging.info("Движение вниз")
    transposed_grid = transpose(grid)
    reversed_grid = reverse(transposed_grid)
    new_grid, changed1 = compress(reversed_grid)
    new_grid, changed2 = merge(new_grid)
    changed = changed1 or changed2
    new_grid, temp = compress(new_grid)
    final_reversed_grid = reverse(new_grid)
    final_grid = transpose(final_reversed_grid)
    logging.info(f"Матрица после движения вниз: {final_grid}")
    return final_grid, changed


def move_right(grid):
    logging.info("Движение вправо")
    reversed_grid = reverse(grid)
    new_grid, changed1 = compress(reversed_grid)
    new_grid, changed2 = merge(new_grid)
    changed = changed1 or changed2
    new_grid, temp = compress(new_grid)
    final_grid = reverse(new_grid)
    logging.info(f"Матрица после движения вправо: {final_grid}")
    return final_grid, changed


def move_left(grid):
    logging.info("Движение влево")
    new_grid, changed1 = compress(grid)
    new_grid, changed2 = merge(new_grid)
    changed = changed1 or changed2
    new_grid, temp = compress(new_grid)
    logging.info(f"Матрица после движения влево: {new_grid}")
    return new_grid, changed


def get_current_state(mat):
    logging.info("Проверка текущего состояния игры")
    # Anywhere 2048 is present
    for i in range(4):
        for j in range(4):
            if (mat[i][j] == 2048):
                return 'WON'
    # Anywhere 0 is present
    for i in range(4):
        for j in range(4):
            if (mat[i][j] == 0):
                return 'GAME NOT OVER'
    # Every Row and Column except last row and last column
    for i in range(3):
        for j in range(3):
            if (mat[i][j] == mat[i+1][j] or mat[i][j] == mat[i][j+1]):
                return 'GAME NOT OVER'
    # Last Row
    for j in range(3):
        if mat[3][j] == mat[3][j+1]:
            return 'GAME NOT OVER'
    # Last Column

    for i in range(3):
        if mat[i][3] == mat[i+1][3]:
            return 'GAME NOT OVER'

    return 'LOST'
