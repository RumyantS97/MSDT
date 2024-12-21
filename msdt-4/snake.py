import random
from typing import List, Tuple

import pygame


pygame.init()

from const import (BLACK,
                   BLOCK_SIZE,
                   BLUE, 
                   RED, 
                   GREEN, 
                   SCREEN_HEIGHT, 
                   SCREEN_WIDTH, 
                   SNAKE_SPEED)

FONT = pygame.font.SysFont("bahnschrift", 25)
SCORE_FONT = pygame.font.SysFont("comicsansms", 35)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Змейка")


def show_score(score: int) -> None:
    """
    Отображает текущий счет игрока.
    """
    value = SCORE_FONT.render(f"Очки: {score}", True, GREEN)
    screen.blit(value, [10, 10])


def draw_snake(block_size: int, snake_list: List[Tuple[int, int]]) -> None:
    """
    Рисует змейку на экране.
    """
    for x in snake_list:
        pygame.draw.rect(screen, BLUE, [x[0], x[1], block_size, block_size])


def message(msg: str, color: Tuple[int, int, int]) -> None:
    """
    Отображает сообщение на экране.
    """
    mesg = FONT.render(msg, True, color)
    screen.blit(mesg, [SCREEN_WIDTH / 6, SCREEN_HEIGHT / 3])


def game_loop() -> None:
    """
    Основной игровой цикл.
    """
    game_over = False
    game_close = False

    x1, y1 = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
    x1_change, y1_change = 0, 0

    snake_list = []
    length_of_snake = 1

    food_x = round(random.randrange(
        0, SCREEN_WIDTH - BLOCK_SIZE) / 20.0) * 20.0
    food_y = round(random.randrange(
        0, SCREEN_HEIGHT - BLOCK_SIZE) / 20.0) * 20.0

    clock = pygame.time.Clock()

    while not game_over:
        while game_close:
            screen.fill(BLACK)
            message("Вы проиграли!\
                     Нажмите Q для выхода или C для продолжения", RED)
            show_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change, y1_change = -BLOCK_SIZE, 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change, y1_change = BLOCK_SIZE, 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    x1_change, y1_change = 0, -BLOCK_SIZE
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    x1_change, y1_change = 0, BLOCK_SIZE

        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(BLACK)
        pygame.draw.rect(
            screen, GREEN, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        draw_snake(BLOCK_SIZE, snake_list)
        show_score(length_of_snake - 1)
        pygame.display.update()

        if x1 == food_x and y1 == food_y:
            food_x = round(random.randrange(
                0,
                SCREEN_WIDTH - BLOCK_SIZE
            ) / 20.0) * 20.0
            food_y = round(random.randrange(
                0,
                SCREEN_HEIGHT - BLOCK_SIZE
            ) / 20.0) * 20.0
            length_of_snake += 1

        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()


if __name__ == "__main__":
    game_loop()
