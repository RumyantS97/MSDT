import random
import copy
import logging
from tkinter import Canvas, Tk, Event, ALL

from path import LOG_PATH


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [%(funcName)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_PATH, encoding='utf-8')
    ]
)


def init() -> None:
    """
    Initialize the game state
    """
    logging.info("initializing the game")
    print_instructions()
    canvas.data.is_game_over = False
    board = []
    canvas.data.empty_color = "blue"
    for x in range(canvas.data.rows):
        board.append([canvas.data.empty_color] * canvas.data.cols)
    canvas.data.tetris_board = board
    canvas.data.tetris_pieces = tetris_pieces()
    canvas.data.tetris_piece_colors = [
        "red", "yellow", "magenta", "pink", "cyan", "green", "orange"
    ]
    canvas.data.score = 0
    new_falling_piece()
    redraw_all()
    logging.info("game initialized")


def print_instructions() -> None:
    """
    Print game instructions to the console
    """
    print("Welcome to Tetris!")
    print("Use the arrow keys to move Left, Right, and Down.")
    print("Press Up to rotate counter-clockwise")
    print("Press 'r' to restart.")
    print("Press 'q' to end the game.")


def tetris_pieces() -> list[list[list[bool]]]:
    """
    Define all Tetris pieces
    """
    i_piece = [[True, True, True, True]]
    j_piece = [[True, False, False], [True, True, True]]
    l_piece = [[False, False, True], [True, True, True]]
    o_piece = [[True, True], [True, True]]
    s_piece = [[False, True, True], [True, True, False]]
    t_piece = [[False, True, False], [True, True, True]]
    z_piece = [[True, True, False], [False, True, True]]
    return [i_piece, j_piece, l_piece, o_piece, s_piece, t_piece, z_piece]


def new_falling_piece() -> None:
    """
    Generate a new falling Tetris piece and place it at the top of the board
    """
    piece_index = random.randint(0, len(canvas.data.tetris_pieces) - 1)
    color_index = random.randint(0, len(canvas.data.tetris_piece_colors) - 1)

    canvas.data.falling_piece = canvas.data.tetris_pieces[piece_index]
    canvas.data.falling_piece_color = canvas.data.tetris_piece_colors[
        color_index
    ]
    canvas.data.falling_piece_row = 0
    canvas.data.falling_piece_col = (
        canvas.data.cols // 2 - len(canvas.data.falling_piece[0]) // 2
    )
    logging.info(f"new piece created: {canvas.data.falling_piece_color}, "
                 f"position: ({canvas.data.falling_piece_row}, "
                 f"{canvas.data.falling_piece_col})")


def draw_tetris_board() -> None:
    """
    Draw the entire Tetris board on the canvas.
    """
    logging.info("drawing the Tetris board")
    for row in range(len(canvas.data.tetris_board)):
        for col in range(len(canvas.data.tetris_board[0])):
            draw_cell(canvas.data.tetris_board, row, col,
                      canvas.data.tetris_board[row][col])


def draw_cell(board: list[list[str]], row: int, col: int, color: str) -> None:
    """
    Draw a single cell on the canvas
    """
    margin = 5
    cell_size = 30
    left = margin + col * cell_size
    right = left + cell_size
    top = margin + row * cell_size
    bottom = top + cell_size
    canvas.create_rectangle(left, top, right, bottom, fill="black")
    border_size = 0
    canvas.create_rectangle(left + border_size, top + border_size,
                            right - border_size, bottom - border_size,
                            fill=color)
    logging.info(f"drew cell at row={row}, col={col}, color={color}")


def draw_falling_piece() -> None:
    """
    Draw the currently falling Tetris piece on the canvas
    """
    logging.info("drawing the falling piece")
    for row in range(len(canvas.data.falling_piece)):
        for col in range(len(canvas.data.falling_piece[0])):
            if canvas.data.falling_piece[row][col]:
                draw_cell(canvas.data.tetris_board,
                          row + canvas.data.falling_piece_row,
                          col + canvas.data.falling_piece_col,
                          canvas.data.falling_piece_color)


def move_falling_piece(drow: int, dcol: int) -> bool:
    """
    Move the currently falling Tetris piece
    """
    initial_row = canvas.data.falling_piece_row
    initial_col = canvas.data.falling_piece_col
    canvas.data.falling_piece_row += drow
    canvas.data.falling_piece_col += dcol
    if not falling_piece_is_legal():
        canvas.data.falling_piece_row = initial_row
        canvas.data.falling_piece_col = initial_col
        return False
    logging.info(f"piece moved: ({drow}, {dcol}), new position: "
                 f"({canvas.data.falling_piece_row},"
                 f"{canvas.data.falling_piece_col})")
    return True


def falling_piece_is_legal() -> bool:
    """
    Check if the currently falling piece is in a legal position
    """
    logging.debug("checking if the falling piece is in a legal position")
    for row in range(len(canvas.data.falling_piece)):
        for col in range(len(canvas.data.falling_piece[0])):
            if canvas.data.falling_piece[row][col]:
                abs_row = row + canvas.data.falling_piece_row
                abs_col = col + canvas.data.falling_piece_col

                if abs_row >= canvas.data.rows or abs_row < 0:
                    logging.warning(f"illegal position: Row {
                                    abs_row} is out of bounds")
                    return False
                if abs_col >= canvas.data.cols or abs_col < 0:
                    logging.warning(f"illegal position: Col {
                                    abs_col} is out of bounds")
                    return False
                if canvas.data.tetris_board[
                    abs_row
                ][abs_col] != canvas.data.empty_color:
                    logging.warning(f"illegal position: Cell [{
                                    abs_row}, {abs_col}] is occupied")
                    return False
    logging.debug("falling piece is in a legal position")
    return True


def redraw_all() -> None:
    """
    Redraw the entire game state on the canvas.
    """
    remove_full_rows()
    if canvas.data.is_game_over:
        logging.info("displaying 'Game Over' message")
        cx = canvas.data.canvas_width / 2
        cy = canvas.data.canvas_height / 2
        canvas.create_text(cx, cy, text="Game Over!",
                           font=("Helvetica", 32, "bold"))
    else:
        canvas.delete(ALL)
        draw_tetris_board()
        draw_falling_piece()
        draw_score()


def draw_score() -> None:
    """
    Draw the current score on the canvas.
    """
    cx = canvas.data.canvas_width - 80
    cy = 20
    score = f"Score: {canvas.data.score}"
    canvas.create_text(cx, cy, text=score, font=(
        "Helvetica", 12, "bold"), fill="white")


def remove_full_rows() -> None:
    """
    Remove full rows from the Tetris board and update the score.
    """
    full_rows = 0
    new_row = canvas.data.rows - 1
    for old_row in range(canvas.data.rows - 1, 0, -1):
        if canvas.data.empty_color in canvas.data.tetris_board[old_row]:
            canvas.data.tetris_board[new_row] = copy.deepcopy(
                canvas.data.tetris_board[old_row])
            new_row -= 1
        else:
            full_rows += 1
    for x in range(new_row - 1, 0, -1):
        canvas.data.tetris_board[x] = [
            canvas.data.empty_color] * canvas.data.cols
    canvas.data.score += (full_rows ** 2) * 100
    logging.info(f"{full_rows} rows removed, score updated: {
                 canvas.data.score}")


def timer_fired() -> None:
    """
    Handle the timer event to update the game state
    """
    logging.info("timer ticked")
    if not move_falling_piece(1, 0):
        place_falling_piece()
        new_falling_piece()
        if not falling_piece_is_legal():
            canvas.data.is_game_over = True
            logging.info("game over, no legal moves available")
    redraw_all()
    delay = 600
    canvas.after(delay, timer_fired)


def key_pressed(event: Event) -> None:
    """
    Handle key press events for controlling the game
    """
    logging.info(f"key pressed: {event.keysym}")
    if event.char == "q":
        canvas.data.is_game_over = True
        logging.info("game over")
    elif event.char == "r":
        logging.info("game restarted")
        init()
    if not canvas.data.is_game_over:
        if event.keysym == "Down":
            move_falling_piece(1, 0)
        elif event.keysym == "Left":
            move_falling_piece(0, -1)
        elif event.keysym == "Right":
            move_falling_piece(0, 1)
        elif event.keysym == "Up":
            rotate_falling_piece()
    redraw_all()


def place_falling_piece() -> None:
    """
    Place the currently falling piece on the board
    """
    logging.info("placing falling piece on the board")
    for row in range(len(canvas.data.falling_piece)):
        for col in range(len(canvas.data.falling_piece[0])):
            if canvas.data.falling_piece[row][col]:
                canvas.data.tetris_board[
                    int(row + canvas.data.falling_piece_row)
                ][
                    int(col + canvas.data.falling_piece_col)
                ] = canvas.data.falling_piece_color
    logging.info(f"piece placed at row {canvas.data.falling_piece_row}")
    redraw_all()


def rotate_falling_piece() -> None:
    """
    Rotate the currently falling piece counter-clockwise
    """
    logging.info("attempting to rotate falling piece")
    old_piece = canvas.data.falling_piece
    old_row = canvas.data.falling_piece_row
    old_col = canvas.data.falling_piece_col
    old_collen = len(canvas.data.falling_piece[0])
    new_col = old_row
    new_row = (old_collen - 1) - old_col
    old_center_row, old_center_col = falling_piece_center()
    new_piece = turn_counter_clockwise(old_piece)
    canvas.data.falling_piece = new_piece
    canvas.data.falling_piece_row = new_row
    canvas.data.falling_piece_col = new_col
    new_center_row, new_center_col = falling_piece_center()
    canvas.data.falling_piece_row += old_center_row - new_center_row
    canvas.data.falling_piece_col += old_center_col - new_center_col
    if falling_piece_is_legal():
        logging.info(f"piece rotated successfully, new position: "
                     f"({canvas.data.falling_piece_row},"
                     f"{canvas.data.falling_piece_col})")
        draw_falling_piece()
    else:
        logging.warning(
            "illegal rotation attempted, reverting to previous state")
        canvas.data.falling_piece = old_piece
        canvas.data.falling_piece_row = old_row
        canvas.data.falling_piece_col = old_col


def turn_counter_clockwise(piece: list[list[bool]]) -> list[list[bool]]:
    """
    Rotate a given Tetris piece counter-clockwise
    """
    logging.info("rotating piece counterclockwise")
    rotated_piece = [
        [piece[y][x] for y in range(len(piece))]
        for x in range(len(piece[0]))
    ]
    rotated_piece.reverse()
    logging.info(f"piece rotated successfully, new shape: {rotated_piece}")
    return rotated_piece


def falling_piece_center() -> tuple[float, float]:
    """
    Calculate the center position of the currently falling piece
    """
    row = canvas.data.falling_piece_row + len(canvas.data.falling_piece) / 2
    col = canvas.data.falling_piece_col + len(
        canvas.data.falling_piece[0]
    ) / 2
    logging.debug(f"falling piece center calculated: ({row}, {col})")
    return row, col


def run(rows: int, cols: int) -> None:
    """
    Start the Tetris game.
    Initializes the game board, sets up event bindings,
    and starts the main game loop
    """
    logging.info(f"starting game with board size {rows}x{cols}")
    global canvas
    root = Tk()
    margin = 5
    cell_size = 30
    canvas_width = 2 * margin + cols * cell_size
    canvas_height = 2 * margin + rows * cell_size
    canvas = Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()
    root.resizable(width=0, height=0)
    root.canvas = canvas.canvas = canvas

    class Struct:
        pass

    canvas.data = Struct()
    canvas.data.rows = rows
    canvas.data.cols = cols
    canvas.data.canvas_width = canvas_width
    canvas.data.canvas_height = canvas_height
    init()
    root.bind("<Key>", key_pressed)
    if not canvas.data.is_game_over:
        timer_fired()
    logging.info("game loop started")
    root.mainloop()


run(15, 10)
