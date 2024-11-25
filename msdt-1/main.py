import pygame as pg
import random, time, sys
from pygame.locals import *

# Type hints
from typing import Dict, List, Optional, Tuple

FPS: int = 25
WINDOW_W, WINDOW_H = 600, 500
BLOCK, CUP_H, CUP_W = 20, 20, 10

SIDE_FREQ: float = 0.15  # Side movement frequency
DOWN_FREQ: float = 0.1  # Downward movement frequency

SIDE_MARGIN: int = int((WINDOW_W - CUP_W * BLOCK) / 2)
TOP_MARGIN: int = WINDOW_H - (CUP_H * BLOCK) - 5

# Color definitions
COLORS: Tuple[Tuple[int, int, int], ...] = ((0, 0, 225), (0, 225, 0), (225, 0, 0), (225, 225, 0))
LIGHTCOLORS: Tuple[Tuple[int, int, int], ...] = ((30, 30, 255), (50, 255, 50), (255, 30, 30), (255, 255, 30))
WHITE, GRAY, BLACK = (255, 255, 255), (185, 185, 185), (0, 0, 0)
BRD_COLOR, BG_COLOR, TXT_COLOR, TITLE_COLOR, INFO_COLOR = WHITE, BLACK, WHITE, COLORS[3], COLORS[0]

FIG_W, FIG_H = 5, 5
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

def pauseScreen() -> None:
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
    display_surf = pg.display.set_mode((WINDOW_W, WINDOW_H))
    basic_font = pg.font.SysFont('arial', 20)
    big_font = pg.font.SysFont('verdana', 45)
    pg.display.set_caption('Tetris Lite')
    showText('Tetris Lite')
    while True:
        runTetris()
        pauseScreen()
        showText('Game Over')


def runTetris() -> None:
    """
    Main game loop for Tetris.
    """
    cup = emptycup()
    last_move_down = time.time()
    last_side_move = time.time()
    last_fall = time.time()
    going_down, going_left, going_right = False, False, False
    points: int = 0
    level, fall_speed = calcSpeed(points)
    fallingFig = getNewFig()
    nextFig = getNewFig()

    while True:
        if fallingFig is None:
            fallingFig = nextFig
            nextFig = getNewFig()
            last_fall = time.time()

            if not checkPos(cup, fallingFig):
                return  # End game if no space for a new figure

        quitGame()
        for event in pg.event.get():
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    pauseScreen()
                    showText('Пауза')
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
                if event.key == K_LEFT and checkPos(cup, fallingFig, adjX=-1):
                    fallingFig['x'] -= 1
                    going_left = True
                    going_right = False
                    last_side_move = time.time()

                elif event.key == K_RIGHT and checkPos(cup, fallingFig, adjX=1):
                    fallingFig['x'] += 1
                    going_right = True
                    going_left = False
                    last_side_move = time.time()

                # поворачиваем фигуру, если есть место
                elif event.key == K_UP:
                    fallingFig['rotation'] = (fallingFig['rotation'] + 1) % len(figures[fallingFig['shape']])
                    if not checkPos(cup, fallingFig):
                        fallingFig['rotation'] = (fallingFig['rotation'] - 1) % len(figures[fallingFig['shape']])

                # ускоряем падение фигуры
                elif event.key == K_DOWN:
                    going_down = True
                    if checkPos(cup, fallingFig, adjY=1):
                        fallingFig['y'] += 1
                    last_move_down = time.time()

                # мгновенный сброс вниз
                elif event.key == K_RETURN:
                    going_down = False
                    going_left = False
                    going_right = False
                    for i in range(1, CUP_H):
                        if not checkPos(cup, fallingFig, adjY=i):
                            break
                    fallingFig['y'] += i - 1

        # управление падением фигуры при удержании клавиш
        if (going_left or going_right) and time.time() - last_side_move > SIDE_FREQ:
            if going_left and checkPos(cup, fallingFig, adjX=-1):
                fallingFig['x'] -= 1
            elif going_right and checkPos(cup, fallingFig, adjX=1):
                fallingFig['x'] += 1
            last_side_move = time.time()

        if going_down and time.time() - last_move_down > DOWN_FREQ and checkPos(cup, fallingFig, adjY=1):
            fallingFig['y'] += 1
            last_move_down = time.time()


        if time.time() - last_fall > fall_speed: # свободное падение фигуры
            if not checkPos(cup, fallingFig, adjY=1): # проверка "приземления" фигуры
                addToCup(cup, fallingFig) # фигура приземлилась, добавляем ее в содержимое стакана
                points += clearCompleted(cup)
                level, fall_speed = calcSpeed(points)
                fallingFig = None
            else: # фигура пока не приземлилась, продолжаем движение вниз
                fallingFig['y'] += 1
                last_fall = time.time()

        # рисуем окно игры со всеми надписями
        display_surf.fill(BG_COLOR)
        drawTitle()
        gamecup(cup)
        drawInfo(points, level)
        drawnextFig(nextFig)
        if fallingFig != None:
            drawFig(fallingFig)
        pg.display.update()
        fps_clock.tick(FPS)

def txtObjects(text: str, font: pg.font.Font, color: Tuple[int, int, int]) -> Tuple[pg.Surface, pg.Rect]:
    """
    Renders text as a surface and returns its rect.
    """
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def stopGame() -> None:
    """
    Terminates the game and exits the program.
    """
    pg.quit()
    sys.exit()


def checkKeys() -> Optional[int]:
    """
    Checks for key press events.

    Returns:
        Optional[int]: The key code if a key was pressed, otherwise None.
    """
    quitGame()

    for event in pg.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def showText(text: str) -> None:
    """
    Displays a message on the screen, waiting for the player to press a key.
    """
    titleSurf, titleRect = txtObjects(text, big_font, TITLE_COLOR)
    titleRect.center = (int(WINDOW_W / 2) - 3, int(WINDOW_H / 2) - 3)
    display_surf.blit(titleSurf, titleRect)

    pressKeySurf, pressKeyRect = txtObjects('Нажмите любую клавишу для продолжения', basic_font, TITLE_COLOR)
    pressKeyRect.center = (int(WINDOW_W / 2), int(WINDOW_H / 2) + 100)
    display_surf.blit(pressKeySurf, pressKeyRect)

    while checkKeys() == None:
        pg.display.update()
        fps_clock.tick()


def quitGame() -> None:
    """
    Handles quitting the game via user input or system events.
    """
    for event in pg.event.get(QUIT): # проверка всех событий, приводящих к выходу из игры
        stopGame()
    for event in pg.event.get(KEYUP):
        if event.key == K_ESCAPE:
            stopGame()
        pg.event.post(event)


def calcSpeed(points: int) -> Tuple[int, float]:
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


def getNewFig() -> Dict[str, int]:
    """
    Generates a new random Tetris figure.

    Returns:
        Dict[str, int]: A dictionary representing the new figure.
    """
    shape = random.choice(list(figures.keys()))
    newFigure = {'shape': shape,
                'rotation': random.randint(0, len(figures[shape]) - 1),
                'x': int(CUP_W / 2) - int(FIG_W / 2),
                'y': -2,
                'color': random.randint(0, len(COLORS) - 1)}
    return newFigure


def addToCup(cup: List[List[str]], fig: Dict[str, int]) -> None:
    """
    Adds a figure to the cup (game area) after it lands.

    Args:
        cup (List[List[str]]): The game area.
        fig (Dict[str, int]): The figure to be added.
    """
    for x in range(FIG_W):
        for y in range(FIG_H):
            if figures[fig['shape']][fig['rotation']][y][x] != EMPTY:
                cup[x + fig['x']][y + fig['y']] = fig['color']


def emptycup() -> List[List[str]]:
    """
    Creates an empty cup (game area).

    Returns:
        List[List[str]]: A 2D list representing the empty game area.
    """
    cup = []
    for i in range(CUP_W):
        cup.append([EMPTY] * CUP_H)
    return cup


def incup(x: int, y: int) -> bool:
    """
    Checks if coordinates are within the cup.

    Args:
        x (int): X-coordinate.
        y (int): Y-coordinate.

    Returns:
        bool: True if inside the cup, False otherwise.
    """
    return x >= 0 and x < CUP_W and y < CUP_H


def checkPos(cup: List[List[str]], fig: Dict[str, int], adjX: int = 0, adjY: int = 0) -> bool:
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
    for x in range(FIG_W):
        for y in range(FIG_H):
            abovecup = y + fig['y'] + adjY < 0
            if abovecup or figures[fig['shape']][fig['rotation']][y][x] == EMPTY:
                continue
            if not incup(x + fig['x'] + adjX, y + fig['y'] + adjY):
                return False
            if cup[x + fig['x'] + adjX][y + fig['y'] + adjY] != EMPTY:
                return False
    return True


def isCompleted(cup: List[List[str]], y: int) -> bool:
    """
    Checks if a row in the cup is completely filled.

    Args:
        cup (List[List[str]]): The game area.
        y (int): The row index.

    Returns:
        bool: True if the row is filled, False otherwise.
    """
    for x in range(CUP_W):
        if cup[x][y] == EMPTY:
            return False
    return True


def clearCompleted(cup: List[List[str]]) -> int:
    """
    Removes completed rows and shifts rows above downwards.

    Args:
        cup (List[List[str]]): The game area.

    Returns:
        int: The number of removed rows.
    """
    removed_lines = 0
    y = CUP_H - 1
    while y >= 0:
        if isCompleted(cup, y):
           for pushDownY in range(y, 0, -1):
                for x in range(CUP_W):
                    cup[x][pushDownY] = cup[x][pushDownY-1]
           for x in range(CUP_W):
                cup[x][0] = EMPTY
           removed_lines += 1
        else:
            y -= 1
    return removed_lines


def convertCoords(block_x: int, block_y: int) -> Tuple[int, int]:
    """
    Converts game coordinates to pixel coordinates.

    Args:
        block_x (int): Block X-coordinate.
        block_y (int): Block Y-coordinate.

    Returns:
        Tuple[int, int]: Pixel coordinates.
    """
    return (SIDE_MARGIN + (block_x * BLOCK)), (TOP_MARGIN + (block_y * BLOCK))


def drawBlock(block_x: Optional[int], block_y: Optional[int], color: int, pixelx: Optional[int] = None, pixely: Optional[int] = None) -> None:
    """
    Draws a single block on the screen.
    """
    if color == EMPTY:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertCoords(block_x, block_y)
    pg.draw.rect(display_surf, COLORS[color], (pixelx + 1, pixely + 1, BLOCK - 1, BLOCK - 1), 0, 3)
    pg.draw.rect(display_surf, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BLOCK - 4, BLOCK - 4), 0, 3)
    pg.draw.circle(display_surf, COLORS[color], (pixelx + BLOCK / 2, pixely + BLOCK / 2), 5)


def gamecup(cup: List[List[str]]) -> None:
    """
    Draws the game area with blocks and borders.
    """
    pg.draw.rect(display_surf, BRD_COLOR, (SIDE_MARGIN - 4, TOP_MARGIN - 4, (CUP_W * BLOCK) + 8, (CUP_H * BLOCK) + 8), 5)
    pg.draw.rect(display_surf, BG_COLOR, (SIDE_MARGIN, TOP_MARGIN, BLOCK * CUP_W, BLOCK * CUP_H))
    for x in range(CUP_W):
        for y in range(CUP_H):
            drawBlock(x, y, cup[x][y])


def drawTitle() -> None:
    """
    Displays the title on the screen.
    """
    titleSurf = big_font.render('Тетрис Lite', True, TITLE_COLOR)
    titleRect = titleSurf.get_rect()
    titleRect.topleft = (WINDOW_W - 425, 30)
    display_surf.blit(titleSurf, titleRect)


def drawInfo(points: int, level: int) -> None:
    """
    Displays the game information such as points and level.
    """
    pointsSurf = basic_font.render(f'Баллы: {points}', True, TXT_COLOR)
    pointsRect = pointsSurf.get_rect()
    pointsRect.topleft = (WINDOW_W - 550, 180)
    display_surf.blit(pointsSurf, pointsRect)

    levelSurf = basic_font.render(f'Уровень: {level}', True, TXT_COLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOW_W - 550, 250)
    display_surf.blit(levelSurf, levelRect)

    pausebSurf = basic_font.render('Пауза: пробел', True, INFO_COLOR)
    pausebRect = pausebSurf.get_rect()
    pausebRect.topleft = (WINDOW_W - 550, 420)
    display_surf.blit(pausebSurf, pausebRect)

    escbSurf = basic_font.render('Выход: Esc', True, INFO_COLOR)
    escbRect = escbSurf.get_rect()
    escbRect.topleft = (WINDOW_W - 550, 450)
    display_surf.blit(escbSurf, escbRect)


def drawFig(fig: Dict[str, int], pixelx: Optional[int] = None, pixely: Optional[int] = None) -> None:
    """
    Draws a Tetris figure on the screen.
    """
    figToDraw = figures[fig['shape']][fig['rotation']]
    if pixelx == None and pixely == None:
        pixelx, pixely = convertCoords(fig['x'], fig['y'])

    #отрисовка элементов фигур
    for x in range(FIG_W):
        for y in range(FIG_H):
            if figToDraw[y][x] != EMPTY:
                drawBlock(None, None, fig['color'], pixelx + (x * BLOCK), pixely + (y * BLOCK))


def drawnextFig(fig: Dict[str, int]) -> None:
    """
    Displays the preview of the next Tetris figure.
    """
    nextSurf = basic_font.render('Следующая:', True, TXT_COLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOW_W - 150, 180)
    display_surf.blit(nextSurf, nextRect)
    drawFig(fig, pixelx=WINDOW_W - 150, pixely=230)


if __name__ == '__main__':
    main()
