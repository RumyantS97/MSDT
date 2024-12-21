import math

import pygame

from pygame import font

pygame.init()
font = pygame.font.SysFont("Arial", 24)
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("3D Sphere (Isometric Projection)")

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
center_x = 350
center_y = height // 2

radius = 200
translation = [0, 0, 0]
rotation_angle = [0, 0, 0]
scale_factor = [1, 1, 1]
grid_size = 10
depth = 5


def drawings():
    draw_axes()
    draw_tree()
    draw_button("Перемещение", 700, 400, 200, 45)
    draw_button("Поворот", 700, 460, 200, 45)
    draw_button("Масштабирование", 700, 520, 200, 45)
    draw_button("X", 905, 340, 90, 50)
    draw_button("Y", 1005, 340, 90, 50)
    draw_button("Z", 1105, 340, 90, 50)

    draw_button("+", 905, 400, 45, 45)
    draw_button("-", 955, 400, 45, 45)
    draw_button("+", 1005, 400, 45, 45)
    draw_button("-", 1055, 400, 45, 45)
    draw_button("+", 1105, 400, 45, 45)
    draw_button("-", 1155, 400, 45, 45)

    draw_button("+", 905, 460, 45, 45)
    draw_button("-", 955, 460, 45, 45)
    draw_button("+", 1005, 460, 45, 45)
    draw_button("-", 1055, 460, 45, 45)
    draw_button("+", 1105, 460, 45, 45)
    draw_button("-", 1155, 460, 45, 45)

    draw_button("+", 905, 520, 45, 45)
    draw_button("-", 955, 520, 45, 45)
    draw_button("+", 1005, 520, 45, 45)
    draw_button("-", 1055, 520, 45, 45)
    draw_button("+", 1105, 520, 45, 45)
    draw_button("-", 1155, 520, 45, 45)


def iso_projection(x, y, z):
    iso_x = (x - y) * math.cos(math.pi / 6)
    iso_y = (x + y) * math.sin(math.pi / 6) - z
    return iso_x, iso_y


def grid():
    for x in range(-grid_size, grid_size + 1):
        for y in range(-grid_size, grid_size + 1):
            for z in range(-depth, depth + 1):
                iso_x, iso_y = iso_projection(x * 40, y * 40, z * 40)
                # Смещение центра
                iso_x += width // 2
                iso_y += height // 2
                pygame.draw.circle(screen, white, (int(iso_x), int(iso_y)), 3)
    for x in range(-grid_size, grid_size):
        for y in range(-grid_size, grid_size):
            for z in range(-depth):
                # Координаты для точек в сетке
                p1 = points[(x + grid_size) * (2 * grid_size + 1) * (depth + 1) +
                            (y + grid_size) * (depth + 1) + (z + depth)]
                p2 = points[(x + grid_size + 1) * (2 * grid_size + 1) * (depth + 1) +
                            (y + grid_size) * (depth + 1) + (z + depth)]
                p3 = points[(x + grid_size) * (2 * grid_size + 1) * (depth + 1) +
                            (y + grid_size + 1) * (depth + 1) + (z + depth)]
                p4 = points[(x + grid_size) * (2 * grid_size + 1) * (depth + 1) +
                            (y + grid_size) * (depth + 1) + (z + depth + 1)]

                # Рисование линий
                pygame.draw.line(screen, white, p1, p2, 1)  # Линия по x
                pygame.draw.line(screen, white, p1, p3, 1)  # Линия по y
                pygame.draw.line(screen, white, p1, p4, 1)  # Линия по z


def project_to_2d_isometric(x, y, z):
    x_2d = (x - y) * math.sqrt(2) / 2
    y_2d = (x + y - 2 * z) * math.sqrt(6) / 6

    x_2d += center_x
    y_2d += center_y
    return int(x_2d), int(y_2d)


def draw_axes():
    axes_size = 350
    x_axis_end = project_to_2d_isometric(axes_size, 0, 0)
    pygame.draw.line(screen, red, (center_x, center_y), x_axis_end, 3)
    draw_arrow(x_axis_end, red, math.pi / 1.5)
    draw_text(x_axis_end, "X", red)
    draw_scale_marks(x_axis_end, 'X', red)
    # Ось Y
    y_axis_end = project_to_2d_isometric(0, axes_size, 0)
    pygame.draw.line(screen, red, (center_x, center_y), y_axis_end, 3)
    # Рисуем стрелку на оси Y
    draw_arrow(y_axis_end, red, -math.pi / 0.5)  # Угол стрелки -30 градусов
    draw_text((y_axis_end[0]-30, y_axis_end[1]), "Y", red)
    draw_scale_marks(y_axis_end, 'Y', red)
    # Ось Z
    z_axis_end = project_to_2d_isometric(0, 0, axes_size)
    pygame.draw.line(screen, red, (center_x, center_y), z_axis_end, 3)
    # Рисуем стрелку на оси Z
    draw_arrow(z_axis_end, red, math.pi / 0.75)
    draw_text(z_axis_end, "Z", red)
    draw_scale_marks(z_axis_end, 'Z', red)


def draw_arrow(start, color, angle):
    # Конец стрелки
    arrow_size = 25
    x_end = start[0] + arrow_size * math.cos(angle)
    y_end = start[1] - arrow_size * math.sin(angle)

    # Рисуем линию стрелки
    pygame.draw.line(screen, color, start, (x_end, y_end), 3)

    # Рисуем вторую линию стрелки
    angle2 = angle + math.pi / 3  # Второй угол для стрелки (30 градусов)
    x_end2 = start[0] + arrow_size * math.cos(angle2)
    y_end2 = start[1] - arrow_size * math.sin(angle2)

    pygame.draw.line(screen, color, start, (x_end2, y_end2), 3)


def draw_text(position, text, color):
    # Создаем текст
    label = font.render(text, True, color)
    # Вычисляем смещение для правильного расположения текста
    text_rect = label.get_rect(center=(position[0] + 15, position[1] - 15))
    screen.blit(label, text_rect)

    
def draw_scale_marks(axis_end, axis, color):
    # Начальные координаты
    start_x, start_y = center_x, center_y
    axis_end_x, axis_end_y = axis_end
    steps = 5
    # Определяем шаг по осям X, Y и Z
    if axis == 'X':
        for i in range(1, steps):
            x_pos = start_x + (axis_end_x - start_x) / steps * i
            y_pos = start_y + (axis_end_y - start_y) / steps * i
            pygame.draw.line(screen, color, (x_pos, y_pos-10), (x_pos, y_pos + 10), 2)
            draw_text((x_pos, y_pos), str(i), color)
    elif axis == 'Y':
        for i in range(1, steps):  # Рисуем 5 меток
            x_pos = start_x + (axis_end_x - start_x) / steps * i
            y_pos = start_y + (axis_end_y - start_y) / steps * i
            pygame.draw.line(screen, color, (x_pos, y_pos-10), (x_pos, y_pos + 10), 2)
            draw_text((x_pos-30, y_pos), str(i), color)
    elif axis == 'Z':
        for i in range(1, steps):  # Рисуем 5 меток
            x_pos = start_x + (axis_end_x - start_x) / steps * i
            y_pos = start_y + (axis_end_y - start_y) / steps * i
            pygame.draw.line(screen, color, (x_pos-10, y_pos), (x_pos+10, y_pos), 2)
            
            draw_text((x_pos, y_pos), str(i), color)


def rotate_x(x, y, z, angle):
    cos_theta = math.cos(angle)
    sin_theta = math.sin(angle)
    return x, y * cos_theta - z * sin_theta, y * sin_theta + z * cos_theta


def rotate_y(x, y, z, angle):
    cos_theta = math.cos(angle)
    sin_theta = math.sin(angle)
    return x * cos_theta + z * sin_theta, y, -x * sin_theta + z * cos_theta


def rotate_z(x, y, z, angle):
    cos_theta = math.cos(angle)
    sin_theta = math.sin(angle)
    return x * cos_theta - y * sin_theta, x * sin_theta + y * cos_theta, z


def draw_tree():
    scale = 50
    N = 5
    H = 20
    R = 2
    segments = 30  # Количество сегментов (чем больше, тем более гладким будет шар)
    for i in range(segments + 1):
        # Угол вдоль вертикальной оси (от 0 до pi)
        alpha = 2*math.pi * i / segments
        for K in range(segments*N + 1):
            # Угол вдоль горизонтальной оси (от 0 до 2pi)
            k = K/segments/N

            # Вычисляем координаты точки на сфере (сферическая координатная система)
            x = ((k*R*N) % R) * math.sin(alpha) * scale
            y = ((k*R*N) % R) * math.cos(alpha) * scale
            z = H * k * scale
            x, y, z = x * scale_factor[0], y * scale_factor[1], z * scale_factor[2]
            x, y, z = x + translation[0], y + translation[1], z + translation[2]
            x, y, z = rotate_x(x, y, z, rotation_angle[0])
            x, y, z = rotate_y(x, y, z, rotation_angle[1])
            x, y, z = rotate_z(x, y, z, rotation_angle[2])

            x_2d, y_2d = project_to_2d_isometric(x, y, z)

            # Рисуем линии между точками, чтобы создать каркас шара
            if i < segments:
                # Линия по вертикали (между сегментами вдоль оси theta)
                alpha_next = 2 * math.pi * (i+1) / segments
                x_next = ((k * N * R) % R) * math.sin(alpha_next) * scale
                y_next = ((k * N * R) % R) * math.cos(alpha_next) * scale
                z_next = H * k * scale
                x_next, y_next, z_next = x_next * scale_factor[0], y_next * scale_factor[1], z_next * scale_factor[2]
                x_next, y_next, z_next = x_next + translation[0], y_next + translation[1], z_next + translation[2]
                x_next, y_next, z_next = rotate_x(x_next, y_next, z_next, rotation_angle[0])
                x_next, y_next, z_next = rotate_y(x_next, y_next, z_next, rotation_angle[1])
                x_next, y_next, z_next = rotate_z(x_next, y_next, z_next, rotation_angle[2])
                x_2d_next, y_2d_next = project_to_2d_isometric(x_next, y_next, z_next)
                pygame.draw.line(screen, white, (x_2d, y_2d), (x_2d_next, y_2d_next))

            if K < segments*N:
                k = (K+1)/segments/N
                x_next = ((k * N * R) % R) * math.sin(alpha) * scale
                y_next = ((k * N * R) % R) * math.cos(alpha) * scale
                z_next = H * k * scale
                x_next, y_next, z_next = x_next * scale_factor[0], y_next * scale_factor[1], z_next * scale_factor[2]
                x_next, y_next, z_next = x_next + translation[0], y_next + translation[1], z_next + translation[2]
                x_next, y_next, z_next = rotate_x(x_next, y_next, z_next, rotation_angle[0])
                x_next, y_next, z_next = rotate_y(x_next, y_next, z_next, rotation_angle[1])
                x_next, y_next, z_next = rotate_z(x_next, y_next, z_next, rotation_angle[2])
                x_2d_next, y_2d_next = project_to_2d_isometric(x_next, y_next, z_next)
                pygame.draw.line(screen, white, (x_2d, y_2d), (x_2d_next, y_2d_next))


def draw_button(text, x, y, width, height):
    pygame.draw.rect(screen, (255, 125, 125), (x, y, width, height))
    label = font.render(text, True, black)
    screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))
# Функция для проверки нажатия кнопки


def check_button_click(x, y, width, height, mouse_pos):
    mx, my = mouse_pos
    return x < mx < x + width and y < my < y + height


running = True
while running:
    screen.fill(black)
    if any(event.type == pygame.MOUSEBUTTONDOWN for event in pygame.event.get()):
        mouse_pos = pygame.mouse.get_pos()
        while not any(event.type == pygame.MOUSEBUTTONUP for event in pygame.event.get()):
            screen.fill(black)
            drawings()
            grid()
            pygame.display.flip()
            pygame.time.delay(10)
            if check_button_click(905, 400, 45, 45, mouse_pos):
                translation[0] += 10
            if check_button_click(955, 400, 45, 45, mouse_pos):
                translation[0] -= 10
            if check_button_click(1005, 400, 45, 45, mouse_pos):
                translation[1] += 10
            if check_button_click(1055, 400, 45, 45, mouse_pos):
                translation[1] -= 10
            if check_button_click(1105, 400, 45, 45, mouse_pos):
                translation[2] += 10
            if check_button_click(1155, 400, 45, 45, mouse_pos):
                translation[2] -= 10


            if check_button_click(905, 460, 45, 45, mouse_pos) == 1:
                rotation_angle[0] += 0.1
            if check_button_click(955, 460, 45, 45, mouse_pos) == 1:
                rotation_angle[0] -= 0.1
            if check_button_click(1005, 460, 45, 45, mouse_pos) == 1:
                rotation_angle[1] += 0.1
            if check_button_click(1055, 460, 45, 45, mouse_pos) == 1:
                rotation_angle[1] -= 0.1
            if check_button_click(1105, 460, 45, 45, mouse_pos) == 1:
                rotation_angle[2] += 0.1
            if check_button_click(1155, 460, 45, 45, mouse_pos) == 1:
                rotation_angle[2] -= 0.1


            if check_button_click(905, 520, 45, 45, mouse_pos) == 1:
                scale_factor[0] += 0.1
            if check_button_click(955, 520, 45, 45, mouse_pos) == 1:
                scale_factor[0] -= 0.1
            if check_button_click(1005, 520, 45, 45, mouse_pos) == 1:
                scale_factor[1] += 0.1
            if check_button_click(1055, 520, 45, 45, mouse_pos) == 1:
                scale_factor[1] -= 0.1
            if check_button_click(1105, 520, 45, 45, mouse_pos) == 1:
                scale_factor[2] += 0.1
            if check_button_click(1155, 520, 45, 45, mouse_pos) == 1:
                scale_factor[2] -= 0.1
    drawings()
    grid()

    # Обновляем экран
    pygame.display.flip()


# Завершаем работу pygame
pygame.quit()
