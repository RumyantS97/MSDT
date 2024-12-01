import logging
import math

import pygame
import numpy as np
from pygame.locals import K_w, K_a, K_s, K_d, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT, K_q, K_e

from constants import FILEPATH


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [%(funcName)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(FILEPATH, encoding='utf-8')
    ]
)
pygame.init()

# Размер окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ёлочка")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Параметры ёлочки
H = 25  # Высота одного блока
R = 100  # Максимальный радиус
N = 10   # Количество ярусов
BLOCKS = 3  # Количество блоков

def generate_tree_block(H, R, N, start_z):
    points = []
    edges = []
    for k in np.linspace(0, 1, N):
        for a in np.linspace(0, 2 * math.pi, N):
            x = (k * N % R) * math.sin(a)
            y = (k * N % R) * math.cos(a)
            z = H * k + start_z
            points.append([x, y, z, 1])
    for i in range(len(points) - N):
        if (i + 1) % N != 0:
            edges.append((i, i + 1))
            edges.append((i, i + N))
    return points, edges

def generate_tree(H, R, N, blocks):
    points = []
    edges = []
    for i in range(blocks):
        block_points, block_edges = generate_tree_block(H, R * (1 - 0.3 * i), N, H * i)
        offset = len(points)
        points.extend(block_points)
        edges.extend([(e[0] + offset, e[1] + offset) for e in block_edges])
    return np.array(points), edges

def apply_transformation(points, transformation_matrix):
    return np.dot(points, transformation_matrix.T)

def scale_matrix(sx, sy, sz):
    return np.array([
        [sx, 0,  0,  0],
        [0,  sy, 0,  0],
        [0,  0,  sz, 0],
        [0,  0,  0,  1]
    ])

def translate_matrix(tx, ty, tz):
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])

def rotate_matrix(axis, angle):
    angle = math.radians(angle)
    if axis == 'x':
        return np.array([
            [1, 0, 0, 0],
            [0, math.cos(angle), -math.sin(angle), 0],
            [0, math.sin(angle), math.cos(angle), 0],
            [0, 0, 0, 1]
        ])
    elif axis == 'y':
        return np.array([
            [math.cos(angle), 0, math.sin(angle), 0],
            [0, 1, 0, 0],
            [-math.sin(angle), 0, math.cos(angle), 0],
            [0, 0, 0, 1]
        ])
    elif axis == 'z':
        return np.array([
            [math.cos(angle), -math.sin(angle), 0, 0],
            [math.sin(angle), math.cos(angle), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

def project_with_perspective(points, zk, znn, width, height):
    projected_points = []
    for point in points:
        x, y, z, _ = point
        x_proj = int((x / (zk - z)) * zk + width // 2)
        y_proj = int((y / (zk - z)) * zk + height // 2)
        projected_points.append((x_proj, y_proj))
    return projected_points

def main():
    clock = pygame.time.Clock()
    points, edges = generate_tree(H, R, N, BLOCKS)
    angle_x, angle_y, angle_z = 0, 0, 0
    scale_factor = 1
    tx, ty, tz = 0, 0, 0
    zk = 500  # Положение камеры
    znn = 300  # Плоскость проецирования
    running = True

    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[K_w]:  # Вращение вокруг оси X
            angle_x += 2
        if keys[K_s]:  # Вращение вокруг оси X в обратную сторону
            angle_x -= 2
        if keys[K_a]:  # Вращение вокруг оси Y
            angle_y += 2
        if keys[K_d]:  # Вращение вокруг оси Y в обратную сторону
            angle_y -= 2
        if keys[K_q]:  # Вращение вокруг оси Z
            angle_z += 2
        if keys[K_e]:  # Вращение вокруг оси Z в обратную сторону
            angle_z -= 2
        if keys[K_UP]:  # Масштабирование увеличение
            scale_factor += 0.05
        if keys[K_DOWN]:  # Масштабирование уменьшение
            scale_factor -= 0.05
        if keys[K_LEFT]:  # Перемещение влево
            tx -= 10
        if keys[K_RIGHT]:  # Перемещение вправо
            tx += 10

        transformation = (
            translate_matrix(tx, ty, tz) @
            scale_matrix(scale_factor, scale_factor, scale_factor) @
            rotate_matrix('x', angle_x) @
            rotate_matrix('y', angle_y) @
            rotate_matrix('z', angle_z)
        )
        transformed_points = apply_transformation(points, transformation)

        projected_points = project_with_perspective(transformed_points, zk, znn, WIDTH, HEIGHT)

        for edge in edges:
            pygame.draw.line(screen, WHITE, projected_points[edge[0]], projected_points[edge[1]], 1)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
