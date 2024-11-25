import random
import sys
import time
import pygame as pg

from pygame.locals import *
from typing import Dict, List, Optional, Tuple


FPS: int = 25
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 500
BLOCK, CUP_HEIGHT, CUP_WIDTH = 20, 20, 10

SIDE_FREQUENCY: float = 0.15  # Side movement frequency
DOWN_FREQUENCY: float = 0.1  # Downward movement frequency

SIDE_MARGIN: int = int((WINDOW_WIDTH - CUP_WIDTH * BLOCK) / 2)
TOP_MARGIN: int = WINDOW_HEIGHT - (CUP_HEIGHT * BLOCK) - 5

# Color definitions
COLORS: Tuple[Tuple[int, int, int], ...] = ((0, 0, 225), (0, 225, 0), (225, 0, 0), (225, 225, 0))
LIGHT_COLORS: Tuple[Tuple[int, int, int], ...] = ((30, 30, 255), (50, 255, 50), (255, 30, 30), (255, 255, 30))
WHITE, GRAY, BLACK = (255, 255, 255), (185, 185, 185), (0, 0, 0)
BOARD_COLOR, BACKGROUND_COLOR, TEXT_COLOR, TITLE_COLOR, INFO_COLOR = WHITE, BLACK, WHITE, COLORS[3], COLORS[0]

FIG_WIDTH, FIG_HEIGHT = 5, 5
EMPTY: str = 'o'

# Tetris figures
figures: Dict[str, List[List[str]]] = {
    'S': [['ooooo', 'ooooo', 'ooxxo', 'oxxoo', 'ooooo'],
          ['ooooo', 'ooxoo', 'ooxxo', 'oooxo', 'ooooo']],
    'Z': [['ooooo', 'ooooo', 'oxxoo', 'ooxxo', 'ooooo'],
          ['ooooo', 'ooxoo', 'oxxoo', 'oxooo', 'ooooo']],
    'J': [['ooooo', 'oxooo', 'oxxxo', 'ooooo', 'ooooo'],
          ['ooooo', 'ooxxo', 'ooxoo', 'ooxoo', 'ooooo'],
          ['ooooo', 'ooooo', 'oxxxo', 'oooxo', 'ooooo'],
          ['ooooo', 'ooxoo', 'ooxoo', 'oxxoo', 'ooooo']],
    'L': [['ooooo', 'oooxo', 'oxxxo', 'ooooo', 'ooooo'],
          ['ooooo', 'ooxoo', 'ooxoo', 'ooxxo', 'ooooo'],
          ['ooooo', 'ooooo', 'oxxxo', 'oxooo', 'ooooo'],
          ['ooooo', 'oxxoo', 'ooxoo', 'ooxoo', 'ooooo']],
    'I': [['ooxoo', 'ooxoo', 'ooxoo', 'ooxoo', 'ooooo'],
          ['ooooo', 'ooooo', 'xxxxo', 'ooooo', 'ooooo']],
    'O': [['ooooo', 'ooooo', 'oxxoo', 'oxxoo', 'ooooo']],
    'T': [['ooooo', 'ooxoo', 'oxxxo', 'ooooo', 'ooooo'],
          ['ooooo', 'ooxoo', 'ooxxo', 'ooxoo', 'ooooo'],
          ['ooooo', 'ooooo', 'oxxxo', 'ooxoo', 'ooooo'],
          ['ooooo', 'ooxoo', 'oxxoo', 'ooxoo', 'ooooo']]
}

def pause_screen() -> None:
    """
    Displays a semi-transparent pause screen overlay.
    """
    pause = pg.Surface((600, 500), pg.SRCALPHA)
    pause.fill((0, 0, 255, 127))
    display_surf.blit(pause, (0, 0))


def main() -> None:
    """
    Main function to initialize the game and control its flow.
    """
    global fps_clock, display_surf, basic_font, big_font
    pg.init()
    fps_clock = pg.time.Clock()
    display_surf = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    basic_font = pg.font.SysFont('arial', 20)
    big_font = pg.font.SysFont('verdana', 45)
    pg.display.set_caption('Tetris Lite')
    show_text('Tetris Lite')
    while True:
        run_tetris()
        pause_screen()
        show_text('Game Over')


def run_tetris() -> None:
    """
    Main game loop for Tetris.
    """
    cup = empty_cup()
    last_move_down = time.time()
    last_side_move = time.time()
    last_fall = time.time()
    going_down, going_left, going_right = False, False, False
    points: int = 0
    level, fall_speed = calc_speed(points)
    falling_fig = get_new_fig()
    next_fig = get_new_fig()

    while True:
        if falling_fig is None:
            falling_fig = next_fig
            next_fig = get_new_fig()
            last_fall = time.time()

            if not check_pos(cup, falling_fig):
                return  # End game if no space for a new figure

        quit_game()
        for event in pg.event.get():
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    pause_screen()
                    show_text('Пауза')
                    last_fall = time.time()
                    last_move_down = time.time()
                    last_side_move = time.time()
                elif event.key == K_LEFT:
                    going_left = False
                elif event.key == K_RIGHT:
                    going_right = False
                elif event.key == K_DOWN:
                    going_down = False

            elif event.type == KEYDOWN:
                # перемещение фигуры вправо и влево
                if event.key == K_LEFT and check_pos(cup, falling_fig, adjX=-1):
                    falling_fig['x'] -= 1
                    going_left = True
                    going_right = False
                    last_side_move = time.time()

                elif event.key == K_RIGHT and check_pos(cup, falling_fig, adjX=1):
                    falling_fig['x'] += 1
                    going_right = True
                    going_left = False
                    last_side_move = time.time()

                # поворачиваем фигуру, если есть место
                elif event.key == K_UP:
                    falling_fig['rotation'] = (falling_fig['rotation'] + 1) % len(figures[falling_fig['shape']])
                    if not check_pos(cup, falling_fig):
                        falling_fig['rotation'] = (falling_fig['rotation'] - 1) % len(figures[falling_fig['shape']])

                # ускоряем падение фигуры
                elif event.key == K_DOWN:
                    going_down = True
                    if check_pos(cup, falling_fig, adjY=1):
                        falling_fig['y'] += 1
                    last_move_down = time.time()

                # мгновенный сброс вниз
                elif event.key == K_RETURN:
                    going_down = False
                    going_left = False
                    going_right = False
                    for i in range(1, CUP_HEIGHT):
                        if not check_pos(cup, falling_fig, adjY=i):
                            break
                    falling_fig['y'] += i - 1

        # управление падением фигуры при удержании клавиш
        if (going_left or going_right) and time.time() - last_side_move > SIDE_FREQUENCY:
            if going_left and check_pos(cup, falling_fig, adjX=-1):
                falling_fig['x'] -= 1
            elif going_right and check_pos(cup, falling_fig, adjX=1):
                falling_fig['x'] += 1
            last_side_move = time.time()

        if going_down and time.time() - last_move_down > DOWN_FREQUENCY and check_pos(cup, falling_fig, adjY=1):
            falling_fig['y'] += 1
            last_move_down = time.time()


        if time.time() - last_fall > fall_speed: # свободное падение фигуры
            if not check_pos(cup, falling_fig, adjY=1): # проверка "приземления" фигуры
                add_to_cup(cup, falling_fig) # фигура приземлилась, добавляем ее в содержимое стакана
                points += clear_completed(cup)
                level, fall_speed = calc_speed(points)
                falling_fig = None
            else: # фигура пока не приземлилась, продолжаем движение вниз
                falling_fig['y'] += 1
                last_fall = time.time()

        # рисуем окно игры со всеми надписями
        display_surf.fill(BACKGROUND_COLOR)
        draw_title()
        game_cup(cup)
        draw_info(points, level)
        draw_next_fig(next_fig)
        if falling_fig != None:
            draw_fig(falling_fig)
        pg.display.update()
        fps_clock.tick(FPS)

def text_objects(text: str, font: pg.font.Font, color: Tuple[int, int, int]) -> Tuple[pg.Surface, pg.Rect]:
    """
    Renders text as a surface and returns its rect.
    """
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def stop_game() -> None:
    """
    Terminates the game and exits the program.
    """
    pg.quit()
    sys.exit()


def check_keys() -> Optional[int]:
    """
    Checks for key press events.

    Returns:
        Optional[int]: The key code if a key was pressed, otherwise None.
    """
    quit_game()

    for event in pg.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def show_text(text: str) -> None:
    """
    Displays a message on the screen, waiting for the player to press a key.
    """
    title_surf, title_rect = text_objects(text, big_font, TITLE_COLOR)
    title_rect.center = (int(WINDOW_WIDTH / 2) - 3, int(WINDOW_HEIGHT / 2) - 3)
    display_surf.blit(title_surf, title_rect)

    press_key_surf, press_key_rect = text_objects('Нажмите любую клавишу для продолжения', basic_font, TITLE_COLOR)
    press_key_rect.center = (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2) + 100)
    display_surf.blit(press_key_surf, press_key_rect)

    while check_keys() == None:
        pg.display.update()
        fps_clock.tick()


def quit_game() -> None:
    """
    Handles quitting the game via user input or system events.
    """
    for event in pg.event.get(QUIT): # проверка всех событий, приводящих к выходу из игры
        stop_game()
    for event in pg.event.get(KEYUP):
        if event.key == K_ESCAPE:
            stop_game()
        pg.event.post(event)


def calc_speed(points: int) -> Tuple[int, float]:
    """
    Calculates the game level and fall speed based on points.

    Args:
        points (int): The player's current score.

    Returns:
        Tuple[int, float]: The current level and the fall speed.
    """
    level = int(points / 10) + 1
    fall_speed = 0.27 - (level * 0.02)
    return level, fall_speed


def get_new_fig() -> Dict[str, int]:
    """
    Generates a new random Tetris figure.

    Returns:
        Dict[str, int]: A dictionary representing the new figure.
    """
    shape = random.choice(list(figures.keys()))
    new_figure = {'shape': shape,
                'rotation': random.randint(0, len(figures[shape]) - 1),
                'x': int(CUP_WIDTH / 2) - int(FIG_WIDTH / 2),
                'y': -2,
                'color': random.randint(0, len(COLORS) - 1)}
    return new_figure


def add_to_cup(cup: List[List[str]], fig: Dict[str, int]) -> None:
    """
    Adds a figure to the cup (game area) after it lands.

    Args:
        cup (List[List[str]]): The game area.
        fig (Dict[str, int]): The figure to be added.
    """
    for x in range(FIG_WIDTH):
        for y in range(FIG_HEIGHT):
            if figures[fig['shape']][fig['rotation']][y][x] != EMPTY:
                cup[x + fig['x']][y + fig['y']] = fig['color']


def empty_cup() -> List[List[str]]:
    """
    Creates an empty cup (game area).

    Returns:
        List[List[str]]: A 2D list representing the empty game area.
    """
    cup = []
    for i in range(CUP_WIDTH):
        cup.append([EMPTY] * CUP_HEIGHT)
    return cup


def in_cup(x: int, y: int) -> bool:
    """
    Checks if coordinates are within the cup.

    Args:
        x (int): X-coordinate.
        y (int): Y-coordinate.

    Returns:
        bool: True if inside the cup, False otherwise.
    """
    return x >= 0 and x < CUP_WIDTH and y < CUP_HEIGHT


def check_pos(cup: List[List[str]], fig: Dict[str, int], adjX: int = 0, adjY: int = 0) -> bool:
    """
    Checks if a figure can occupy a specific position in the cup.

    Args:
        cup (List[List[str]]): The game area.
        fig (Dict[str, int]): The figure.
        adjX (int): Horizontal adjustment. Default is 0.
        adjY (int): Vertical adjustment. Default is 0.

    Returns:
        bool: True if the position is valid, False otherwise.
    """
    for x in range(FIG_WIDTH):
        for y in range(FIG_HEIGHT):
            above_cup = y + fig['y'] + adjY < 0
            if above_cup or figures[fig['shape']][fig['rotation']][y][x] == EMPTY:
                continue
            if not in_cup(x + fig['x'] + adjX, y + fig['y'] + adjY):
                return False
            if cup[x + fig['x'] + adjX][y + fig['y'] + adjY] != EMPTY:
                return False
    return True


def is_completed(cup: List[List[str]], y: int) -> bool:
    """
    Checks if a row in the cup is completely filled.

    Args:
        cup (List[List[str]]): The game area.
        y (int): The row index.

    Returns:
        bool: True if the row is filled, False otherwise.
    """
    for x in range(CUP_WIDTH):
        if cup[x][y] == EMPTY:
            return False
    return True


def clear_completed(cup: List[List[str]]) -> int:
    """
    Removes completed rows and shifts rows above downwards.

    Args:
        cup (List[List[str]]): The game area.

    Returns:
        int: The number of removed rows.
    """
    removed_lines = 0
    y = CUP_HEIGHT - 1
    while y >= 0:
        if is_completed(cup, y):
           for push_down_y in range(y, 0, -1):
                for x in range(CUP_WIDTH):
                    cup[x][push_down_y] = cup[x][push_down_y-1]
           for x in range(CUP_WIDTH):
                cup[x][0] = EMPTY
           removed_lines += 1
        else:
            y -= 1
    return removed_lines


def convert_coords(block_x: int, block_y: int) -> Tuple[int, int]:
    """
    Converts game coordinates to pixel coordinates.

    Args:
        block_x (int): Block X-coordinate.
        block_y (int): Block Y-coordinate.

    Returns:
        Tuple[int, int]: Pixel coordinates.
    """
    return (SIDE_MARGIN + (block_x * BLOCK)), (TOP_MARGIN + (block_y * BLOCK))


def draw_block(block_x: Optional[int], block_y: Optional[int], color: int, pixelx: Optional[int] = None, pixely: Optional[int] = None) -> None:
    """
    Draws a single block on the screen.
    """
    if color == EMPTY:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convert_coords(block_x, block_y)
    pg.draw.rect(display_surf, COLORS[color], (pixelx + 1, pixely + 1, BLOCK - 1, BLOCK - 1), 0, 3)
    pg.draw.rect(display_surf, LIGHT_COLORS[color], (pixelx + 1, pixely + 1, BLOCK - 4, BLOCK - 4), 0, 3)
    pg.draw.circle(display_surf, COLORS[color], (pixelx + BLOCK / 2, pixely + BLOCK / 2), 5)


def game_cup(cup: List[List[str]]) -> None:
    """
    Draws the game area with blocks and borders.
    """
    pg.draw.rect(display_surf, BOARD_COLOR, (SIDE_MARGIN - 4, TOP_MARGIN - 4, (CUP_WIDTH * BLOCK) + 8, (CUP_HEIGHT * BLOCK) + 8), 5)
    pg.draw.rect(display_surf, BACKGROUND_COLOR, (SIDE_MARGIN, TOP_MARGIN, BLOCK * CUP_WIDTH, BLOCK * CUP_HEIGHT))
    for x in range(CUP_WIDTH):
        for y in range(CUP_HEIGHT):
            draw_block(x, y, cup[x][y])


def draw_title() -> None:
    """
    Displays the title on the screen.
    """
    title_surf = big_font.render('Тетрис Lite', True, TITLE_COLOR)
    title_rect = title_surf.get_rect()
    title_rect.topleft = (WINDOW_WIDTH - 425, 30)
    display_surf.blit(title_surf, title_rect)


def draw_info(points: int, level: int) -> None:
    """
    Displays the game information such as points and level.
    """
    points_surf = basic_font.render(f'Баллы: {points}', True, TEXT_COLOR)
    points_rect = points_surf.get_rect()
    points_rect.topleft = (WINDOW_WIDTH - 550, 180)
    display_surf.blit(points_surf, points_rect)

    level_surf = basic_font.render(f'Уровень: {level}', True, TEXT_COLOR)
    level_rect = level_surf.get_rect()
    level_rect.topleft = (WINDOW_WIDTH - 550, 250)
    display_surf.blit(level_surf, level_rect)

    pauseb_surf = basic_font.render('Пауза: пробел', True, INFO_COLOR)
    pauseb_rect = pauseb_surf.get_rect()
    pauseb_rect.topleft = (WINDOW_WIDTH - 550, 420)
    display_surf.blit(pauseb_surf, pauseb_rect)

    escb_surf = basic_font.render('Выход: Esc', True, INFO_COLOR)
    escb_rect = escb_surf.get_rect()
    escb_rect.topleft = (WINDOW_WIDTH - 550, 450)
    display_surf.blit(escb_surf, escb_rect)


def draw_fig(fig: Dict[str, int], pixelx: Optional[int] = None, pixely: Optional[int] = None) -> None:
    """
    Draws a Tetris figure on the screen.
    """
    fig_to_draw = figures[fig['shape']][fig['rotation']]
    if pixelx == None and pixely == None:
        pixelx, pixely = convert_coords(fig['x'], fig['y'])

    #отрисовка элементов фигур
    for x in range(FIG_WIDTH):
        for y in range(FIG_HEIGHT):
            if fig_to_draw[y][x] != EMPTY:
                draw_block(None, None, fig['color'], pixelx + (x * BLOCK), pixely + (y * BLOCK))


def draw_next_fig(fig: Dict[str, int]) -> None:
    """
    Displays the preview of the next Tetris figure.
    """
    next_surf = basic_font.render('Следующая:', True, TEXT_COLOR)
    next_rect = next_surf.get_rect()
    next_rect.topleft = (WINDOW_WIDTH - 150, 180)
    display_surf.blit(next_surf, next_rect)
    draw_fig(fig, pixelx=WINDOW_WIDTH - 150, pixely=230)


if __name__ == '__main__':
    main()
