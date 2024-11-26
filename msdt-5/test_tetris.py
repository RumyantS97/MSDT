import pytest
from main import rotate_clockwise, check_collision, remove_row, join_matrixes, new_board, TetrisApp


@pytest.mark.parametrize("input_shape, expected", [
    ([[1, 0], [1, 1]], [[1, 1], [1, 0]]),  # Простой случай
    ([[1, 1, 1], [0, 1, 0]], [[0, 1], [1, 1], [0, 1]])  # Тетромино "Т"
])
def test_rotate_clockwise(input_shape, expected):
    result = rotate_clockwise(input_shape)
    assert result == expected


@pytest.mark.parametrize("board, shape, offset, expected", [
    ([[0, 0, 0], [0, 0, 0]], [[1, 1], [1, 0]], (1, 0), False),  # Нет столкновений
    ([[1, 0, 0], [0, 0, 0]], [[1, 1], [1, 0]], (0, 0), True)  # Столкновение
])
def test_check_collision(board, shape, offset, expected):
    result = check_collision(board, shape, offset)
    assert result == expected


def test_remove_row():
    board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    expected = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    result = remove_row(board, 1)
    assert result == expected


def test_join_matrixes():
    mat1 = [[0, 0], [0, 0]]
    mat2 = [[1, 1], [0, 1]]
    expected = [[1, 1], [0, 1]]  # Ожидаемый результат объединения
    result = join_matrixes(mat1, mat2, (0, 1))
    assert result == expected


def test_new_board():
    board = new_board()
    assert len(board) == 23  # 22 строки + 1 строка-граница
    assert all(len(row) == 10 for row in board)  # Каждая строка должна содержать 10 элементов


@pytest.fixture
def mock_new_stone(mocker):
    # Мокаем метод new_stone
    app = TetrisApp()
    mocker.patch.object(app, 'new_stone')  # Мокируем метод new_stone
    return app


def test_tetrisapp_new_stone(mock_new_stone):
    mock_new_stone.init_game()  # Инициализация игры, которая вызывает new_stone
    mock_new_stone.new_stone.assert_called_once()  # Проверяем, что new_stone был вызван один раз


@pytest.mark.parametrize("lines_cleared, expected_score", [
    (0, 0), (1, 40), (2, 100), (3, 300), (4, 1200)  # Ожидаемые результаты для разных очисток
])
def test_add_cl_lines(lines_cleared, expected_score):
    app = TetrisApp()
    app.add_cl_lines(lines_cleared)  # Добавляем линии
    assert app.score == expected_score  # Проверяем, что счет правильный
