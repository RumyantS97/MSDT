import pygame
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [%(funcName)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('msdt-4/Logging.txt', encoding='utf-8')
    ]
)


pygame.init()


width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Лабораторная работа 3')


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)


center_x, center_y = width // 2, height // 2


scale_factor = 20


running = True


def draw_axes():
    logging.info("Drawing axes")
    pygame.draw.line(screen, BLACK, (0, center_y), (width, center_y), 2)
    pygame.draw.line(screen, BLACK, (center_x, 0), (center_x, height), 2)
    for x in range(center_x, width, 50):
        pygame.draw.line(screen, GRAY, (x, center_y - 5), (x, center_y + 5), 1)
    for x in range(center_x, 0, -50):
        pygame.draw.line(screen, GRAY, (x, center_y - 5), (x, center_y + 5), 1)
    for y in range(center_y, height, 50):
        pygame.draw.line(screen, GRAY, (center_x - 5, y), (center_x + 5, y), 1)
    for y in range(center_y, 0, -50):
        pygame.draw.line(screen, GRAY, (center_x - 5, y), (center_x + 5, y), 1)


def get_input_text(prompt):
    logging.info(f"Requesting input: {prompt}")
    input_text = ""
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.warning("Application quit during input")
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode.isdigit() or (event.unicode == "-" and not input_text):
                    input_text += event.unicode

        screen.fill(WHITE)
        draw_axes()
        text_surface = font.render(f"{prompt} {input_text}", True, BLACK)
        screen.blit(text_surface, (20, 20))
        pygame.display.flip()
        clock.tick(30)

    logging.info(f"Input received: {input_text}")
    return int(input_text) if input_text.isdigit() else 0


def draw_line(x1, y1, x2, y2, color=BLACK):
    logging.info(f"Drawing line from ({x1}, {y1}) to ({x2}, {y2})")
    x1 += center_x
    y1 = center_y - y1
    x2 += center_x
    y2 = center_y - y2
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    while True:
        screen.set_at((x1, y1), color)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
    logging.info("Line drawn successfully")


def draw_circle(xc, yc, r, color=BLACK):
    logging.info(f"Drawing circle at ({xc}, {yc}) with radius {r}")
    xc += center_x
    yc = center_y - yc
    r *= scale_factor
    x = 0
    y = r
    d = 3 - 2 * r

    def plot_circle_points(xc, yc, x, y):
        screen.set_at((xc + x, yc + y), color)
        screen.set_at((xc - x, yc + y), color)
        screen.set_at((xc + x, yc - y), color)
        screen.set_at((xc - x, yc - y), color)
        screen.set_at((xc + y, yc + x), color)
        screen.set_at((xc - y, yc + x), color)
        screen.set_at((xc + y, yc - x), color)
        screen.set_at((xc - y, yc - x), color)

    while x <= y:
        plot_circle_points(xc, yc, x, y)
        if d <= 0:
            d = d + 4 * x + 6
        else:
            d = d + 4 * (x - y) + 10
            y -= 1
        x += 1
    logging.info("Circle drawn successfully")


def draw_bezier(p1, p2, p3, p4, color=BLACK):
    logging.info(f"Drawing Bezier curve with points {p1}, {p2}, {p3}, {p4}")
    points = []
    for t in range(1001):
        t /= 1000.0
        x = (1 - t) ** 3 * p1[0] + 3 * (1 - t) ** 2 * t * \
            p2[0] + 3 * (1 - t) * t ** 2 * p3[0] + t ** 3 * p4[0]
        y = (1 - t) ** 3 * p1[1] + 3 * (1 - t) ** 2 * t * \
            p2[1] + 3 * (1 - t) * t ** 2 * p3[1] + t ** 3 * p4[1]
        points.append((center_x + int(x * scale_factor),
                      center_y - int(y * scale_factor)))
    pygame.draw.lines(screen, color, False, points, 2)
    logging.info("Bezier curve drawn successfully")


def scanline_fill(points, color):
    logging.info(f"Filling polygon with points {points} and color {color}")
    points = [(center_x + x, center_y - y) for x, y in points]
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)
    for y in range(min_y, max_y + 1):
        intersections = []
        for i in range(len(points)):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % len(points)]
            if y1 == y2:
                continue
            if y1 <= y < y2 or y2 <= y < y1:
                x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                intersections.append(int(x))
        intersections.sort()
        for i in range(0, len(intersections) - 1, 2):
            pygame.draw.line(
                screen, color, (intersections[i], y), (intersections[i + 1], y), 1)
    logging.info("Polygon filled successfully")


def pattern_fill(x, y, color1, color2):
    logging.info(f"Pattern fill starting at ({x}, {
                 y}) with colors {color1} and {color2}")
    x, y = center_x + x, center_y - y
    target_color = screen.get_at((x, y))
    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        if (0 <= cx < width and 0 <= cy < height) and screen.get_at((cx, cy)) == target_color:
            fill_color = color1 if (cx + cy) % 2 == 0 else color2
            screen.set_at((cx, cy), fill_color)
            stack.extend([(cx + 1, cy), (cx - 1, cy),
                         (cx, cy + 1), (cx, cy - 1)])
    logging.info("Pattern fill completed successfully")


def main():
    global running
    logging.info("Application started")
    while running:
        screen.fill(WHITE)
        draw_axes()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.info("Application quit event received")
                running = False

        print("1. Draw a line\n2. Draw a circle\n3. Draw a Bezier curve\n4. Polygon fill\n5. Pattern fill\n0. Exit")
        choice = input("Enter your choice (1-5, 0 to exit): ").strip()
        logging.info(f"User choice: {choice}")

        if choice == "1":
            x1, y1 = get_input_text("x1:"), get_input_text("y1:")
            x2, y2 = get_input_text("x2:"), get_input_text("y2:")
            draw_line(x1, y1, x2, y2, RED)
        elif choice == "2":
            xc, yc = get_input_text("xc:"), get_input_text("yc:")
            r = get_input_text("Radius:")
            draw_circle(xc, yc, r, BLACK)
        elif choice == "3":
            p1 = (get_input_text("x1:"), get_input_text("y1:"))
            p2 = (get_input_text("x2:"), get_input_text("y2:"))
            p3 = (get_input_text("x3:"), get_input_text("y3:"))
            p4 = (get_input_text("x4:"), get_input_text("y4:"))
            draw_bezier(p1, p2, p3, p4, BLUE)
        elif choice == "4":
            points = []
            print("Enter polygon points. Repeat the first point to close:")
            while True:
                x, y = get_input_text("x:"), get_input_text("y:")
                if points and (x, y) == points[0]:
                    break
                points.append((x, y))
            color = (get_input_text("R:"), get_input_text(
                "G:"), get_input_text("B:"))
            scanline_fill(points, color)
        elif choice == "5":
            x = get_input_text("x (inside area):")
            y = get_input_text("y (inside area):")
            color1 = (get_input_text("R1:"), get_input_text(
                "G1:"), get_input_text("B1:"))
            color2 = (get_input_text("R2:"), get_input_text(
                "G2:"), get_input_text("B2:"))
            pattern_fill(x, y, color1, color2)
        elif choice == "0":
            logging.info("Exiting application")
            running = False
        else:
            logging.warning(f"Invalid choice: {choice}")

        pygame.display.flip()


if __name__ == "__main__":
    main()
    pygame.quit()
    logging.info("Application closed")
