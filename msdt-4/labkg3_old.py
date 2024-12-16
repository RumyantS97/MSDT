import pygame
import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler("cat_drawing.log"),  # Запись в файл
    logging.StreamHandler()  # Вывод в консоль
])

# Инициализация
pygame.init()
logging.info("Pygame initialized.")
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
screen.fill((255, 255, 255))
pygame.display.set_caption("Кот грустит")
logging.info("Window created with size %dx%d", width, height)

pattern = [
    [(255, 182, 193), (255, 0, 0)],  # Светло-розовый и красный
    [(255, 0, 0), (255, 182, 193)]  # Красный и светло-розовый
]


# Естественный алгоритм рисования линии
def natural_line(x0, y0, x1, y1, color):
    logging.debug(f"Drawing natural line from ({x0}, {y0}) to ({x1}, {y1}) with color {color}")
    dx, dy = x1 - x0, y1 - y0
    steps = max(abs(dx), abs(dy))
    for i in range(steps + 1):
        x = round(x0 + i * dx / steps)
        y = round(y0 + i * dy / steps)
        screen.set_at((x, y), color)
    logging.debug(f"Line drawn: {steps} steps.")


# Алгоритм Брезенхама для линии
def bresenham_line(x0, y0, x1, y1, color):
    logging.debug(f"Drawing Bresenham line from ({x0}, {y0}) to ({x1}, {y1}) with color {color}")
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        screen.set_at((x0, y0), color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
    logging.debug(f"Bresenham line drawn.")


# Алгоритм Брезенхама для окружности
def bresenham_circle(xc, yc, r, color):
    logging.debug(f"Drawing Bresenham circle at ({xc}, {yc}) with radius {r} and color {color}")
    x, y, d = 0, r, 3 - 2 * r
    while x <= y:
        for x_sym, y_sym in [
            (x, y), (y, x), (-x, y), (-y, x), (-x, -y), (-y, -x), (x, -y), (y, -x)
        ]:
            screen.set_at((xc + x_sym, yc + y_sym), color)
        if d < 0:
            d += 4 * x + 6
        else:
            d += 4 * (x - y) + 10
            y -= 1
        x += 1
    logging.debug(f"Bresenham circle drawn.")


# Алгоритм закраски "короедом"
def beetle_fill(x, y, fill_color, boundary_color):
    logging.debug(f"Starting beetle fill at ({x}, {y}) with fill color {fill_color}")
    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        if screen.get_at((cx, cy)) != boundary_color and screen.get_at((cx, cy)) != fill_color:
            screen.set_at((cx, cy), fill_color)
            stack.extend([(cx + dx, cy + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]])
    logging.debug(f"Beetle fill completed.")


# Алгоритм закраски с узором
def fill_pattern(x, y, pattern, boundary_color):
    logging.debug(f"Starting pattern fill at ({x}, {y}) with boundary color {boundary_color}")
    stack = [(x, y)]
    visited = set()

    while stack:
        cx, cy = stack.pop()
        if not (0 <= cx < width and 0 <= cy < height):
            continue
        if (cx, cy) in visited:
            continue
        visited.add((cx, cy))

        current_color = screen.get_at((cx, cy))
        if current_color == boundary_color:
            continue

        # Применяем паттерн
        pattern_x = (cx // 5) % len(pattern)
        pattern_y = (cy // 5) % len(pattern[0])
        screen.set_at((cx, cy), pattern[pattern_x][pattern_y])

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = cx + dx, cy + dy
            if screen.get_at((nx, ny)) != boundary_color and 0 <= nx < width and 0 <= ny < height:
                stack.append((nx, ny))
    logging.debug(f"Pattern fill completed.")


# Модифицированная алгоритм с затравкой
def modified_seed_fill(x, y, pattern, boundary_color):
    logging.debug(f"Starting modified seed fill at ({x}, {y}) with pattern {pattern}")
    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()

        # Закрашивание стрроки вправо и влево
        x_left, x_right = cx, cx
        while x_left >= 0 and screen.get_at((x_left, cy)) != boundary_color:
            screen.set_at((x_left, cy), pattern)
            x_left -= 1
        while x_right < width and screen.get_at((x_right, cy)) != boundary_color:
            screen.set_at((x_right, cy), pattern)
            x_right += 1

        # Обработка строк выше и ниже
        for nx in range(x_left + 1, x_right):
            for ny in (cy - 1, cy + 1):
                if 0 <= ny < height and screen.get_at((nx, ny)) != boundary_color and screen.get_at(
                        (nx, ny)) != pattern:
                    stack.append((nx, ny))
    logging.debug(f"Modified seed fill completed.")


# Рисование морды кота
def draw_cat():
    logging.info("Drawing cat face...")
    pygame.draw.circle(screen, (210, 180, 140), (400, 300), 100)  # Шерсть
    pygame.draw.circle(screen, (0, 0, 0), (400, 300), 100, 1)  # Контур
    logging.info("Contoure drawn.")

    # Уши
    bresenham_line(320, 240, 330, 180, (0, 0, 0))  # Левое ухо
    bresenham_line(330, 180, 360, 210, (0, 0, 0))
    bresenham_line(440, 210, 470, 180, (0, 0, 0))  # Правое ухо
    bresenham_line(470, 180, 480, 240, (0, 0, 0))
    logging.info("Ears drawn.")

    # Глаза
    bresenham_circle(360, 270, 15, (0, 0, 0))
    bresenham_circle(440, 270, 15, (0, 0, 0))
    logging.info("Eyes drawn.")

    # Закраска глаз
    beetle_fill(360, 270, (0, 255, 0), (0, 0, 0))  # Левый глаз
    beetle_fill(440, 270, (0, 255, 0), (0, 0, 0))  # Правый глаз
    logging.info("Eyes filled.")

    # Нос
    natural_line(390, 300, 410, 300, (0, 0, 0))
    natural_line(390, 300, 400, 320, (0, 0, 0))
    natural_line(410, 300, 400, 320, (0, 0, 0))
    logging.info("Nose drawn.")

    # Закраска носа узором
    modified_seed_fill(400, 310, (255, 182, 193), (0, 0, 0))
    logging.info("Nose filled with pattern.")


# Основной цикл
running = True
draw_cat()
pygame.display.flip()
logging.info("Drawing completed. Program running...")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            logging.info("Program terminated.")
pygame.quit()
