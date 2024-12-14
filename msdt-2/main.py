import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from collections import deque
import math


# Функция рисования окружности Брезенхама
def draw_circle(image: np.ndarray, x_center: int, y_center: int, radius: int, color: int):
    x = radius
    y = 0
    d = 3 - 2*radius
    while x > y:
        if x_center + x < image.shape[1] and y_center + y < image.shape[0]:
            image[y_center + y][x_center + x] = color
        if x_center - x >= 0 and y_center + y < image.shape[0]:
            image[y_center + y][x_center - x] = color
        if x_center + y < image.shape[1] and y_center + x < image.shape[0]:
            image[y_center + x][x_center + y] = color
        if x_center - y >= 0 and y_center + x < image.shape[0]:
            image[y_center + x][x_center - y] = color
        if x_center + x < image.shape[1] and y_center - y >= 0:
            image[y_center - y][x_center + x] = color
        if x_center - x >= 0 and y_center - y >= 0:
            image[y_center - y][x_center - x] = color
        if x_center + y < image.shape[1] and y_center - x >= 0:
            image[y_center - x][x_center + y] = color
        if x_center - y >= 0 and y_center - x >= 0:
            image[y_center - x][x_center - y] = color
        if d <= 0:
            d += 4*y + 6
        else:
            d += 4 * (y-x) + 10
            x -= 1
        y += 1


# Функция для рисования линии по естественному алгоритму
def draw_line(image: np.ndarray, x0: int, y0: int, x1: int, y1: int, color: int):
    if abs(x1 - x0) < abs(y1 - y0):
        if y0 > y1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        a = (x1 - x0) / (y1 - y0)
        b = x0 - a * y0
        for y in range(y0, y1 + 1):
            x = int(a * y + b)
            if 0 <= x < image.shape[1] and 0 <= y < image.shape[0]:
                image[y,x] = color
    else:
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        a = (y1 - y0) / (x1 - x0)
        b = y0 - a * x0
        for x in range(x0, x1 + 1):
            y = int(a * x + b)
            if 0 <= x < image.shape[1] and 0 <= y < image.shape[0]:
                image[y,x] = color


# Функция для заполнения области узором
def fill_with_pattern(image: np.ndarray, top_left_x: int, top_left_y: int, bottom_right_x: int, bottom_right_y: int, pattern: np.ndarray):
    pattern_width = pattern.shape[0]
    pattern_height = pattern.shape[1]
    for y in range(top_left_y, bottom_right_y + 1):
        for x in range(top_left_x, bottom_right_x + 1):
            if 0 <= x < image.shape[1] and 0 <= y < image.shape[0]:
                image[y,x] = pattern[x % pattern_width][y % pattern_height]


# Параметрическое построение кривых Безье
def bezier_curve(image, control_points, color):
    num_points = 100
    n = len(control_points)
    t = np.linspace(0, 1, num_points)
    Bx = np.zeros(num_points)
    By = np.zeros(num_points)
    for i in range(n):
        binomial_coeff = math.comb(n-1, i)
        Bx += binomial_coeff * (t ** i) * ((1-t) ** (n-1-i)) * control_points[i][0]
        By += binomial_coeff * (t ** i) * ((1-t) ** (n-1-i)) * control_points[i][1]
    for i in range(num_points):
            x = int(Bx[i])
            y = int(By[i])
            if 0 <= x < w and 0 <= y < h:
                image[y, x] = color


# Функция для закраски области "короедом" с помощью стека
def flood_fill1(image, x, y, contour_color, fill_color):
    stack = deque([(x, y)])
    while stack:
        x, y = stack.pop()
        if (0<x<image.shape[1])&(0<y<image.shape[0]):
            if (image[y, x]!=fill_color)&(image[y, x]!=contour_color):
                image[y, x] = fill_color
                if (image[y, x + 1] != fill_color) & (image[y, x + 1] != contour_color):
                    stack.append((x + 1, y))
                if (image[y, x - 1] != fill_color) & (image[y, x - 1] != contour_color):
                    stack.append((x - 1, y))
                if (image[y + 1, x] != fill_color) & (image[y + 1,x] != contour_color):
                    stack.append((x, y + 1))
                if (image[y - 1, x] != fill_color) & (image[y - 1,x] != contour_color):
                    stack.append((x, y - 1))


# Определение размера рисунка
w = 200
h = 200
# Определение цветовой карты для отображения результата
cmap = ListedColormap(['coral', 'gold', 'black', 'paleturquoise', 'lightseagreen'])
# Создание изображения
image = np.zeros((h, w), dtype=int)
# Параметры окружности
x_center = w // 2
y_center = 3 * h // 10
radius = 50

# Рисунок
draw_circle(image, x_center, y_center, radius, 1)
flood_fill1(image, x_center, y_center, 1, 1)
draw_line(image, 0, h // 2 + h // 4, w - 1, h // 2 + h // 4, 4)
draw_line(image, w - 1, h // 2 + h // 4, w - 1, h, 4)
draw_line(image, w - 1, h - 1, 0, h - 1, 4)
draw_line(image, 0, h, 0, h // 2 + h // 4, 4)

pattern = np.array([
    [4, 3],
    [3, 4]
])
transposed_pattern = pattern.transpose()


def fill_polygon_with_pattern(image: np.ndarray, vertices: np.ndarray, pattern: np.ndarray):
    min_y = int(np.min(vertices[:, 1]))
    max_y = int(np.max(vertices[:, 1]))
    pattern_height, pattern_width = pattern.shape
    for y in range(min_y, max_y + 1):
        intersections = []
        for i in range(len(vertices)):
            p1 = vertices[i]
            p2 = vertices[(i + 1) % len(vertices)]
            if (p1[1] <= y < p2[1]) or (p2[1] <= y < p1[1]):
                x_intersect = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])
                intersections.append(x_intersect)
        intersections.sort()
        for j in range(0, len(intersections), 2):
            if j + 1 < len(intersections):
                x0 = int(np.floor(intersections[j]))
                x1 = int(np.floor(intersections[j + 1]))
                for x in range(x0, x1 + 1):
                    if 0 <= x < image.shape[1] and 0 <= y < image.shape[0]:
                        pattern_x = (x - x0) % pattern_width
                        pattern_y = (y - min_y) % pattern_height
                        if pattern_x < pattern_width and pattern_y < pattern_height:
                            image[y, x] = pattern[pattern_y][pattern_x]


# Определяем вершины полигона
vertices = np.array([[0, h // 2 + h // 4], [w - 1, h // 2 + h // 4], [w - 1, h], [0, h]])
fill_polygon_with_pattern(image, vertices, pattern)

# Рисунок пальм
bezier_curve(image, [(w / 4, h / 4 * 3 - 1), (w / 4 * 2, h / 2), (w / 4 * 3, h / 4 * 3 - 1)], 2)
draw_line(image, 50, 150-1, 150, 150-1, 2)
flood_fill1(image, 100,150-3, 2,2)

bezier_curve(image, [(76, 131),(82,117),(50,80),(59, 50),],2)
bezier_curve(image, [(91, 125),(62,80),(59, 50)],2)
flood_fill1(image, 79,113, 2, 2)

bezier_curve(image, [(60, 57),(73,50),(84, 65)],2)
bezier_curve(image, [(63, 48),(85,48),(84, 65)],2)

bezier_curve(image, [(63, 48),(77,35),(92, 51)],2)
bezier_curve(image, [(63, 37),(84,28),(92, 51)],2)

bezier_curve(image, [(63, 37),(63,28),(75, 25)],2)
bezier_curve(image, [(57, 36),(60,21),(75, 25)],2)

bezier_curve(image, [(56, 36), (50, 21),(36,26)],2)
bezier_curve(image, [(50, 40),(47, 31),(36,26)],2)

bezier_curve(image, [(50, 40),(23, 30),(15,50)],2)
bezier_curve(image, [(50, 45),(30, 40),(15,50)],2)

bezier_curve(image, [(50, 45),(30, 53),(35,70)],2)
bezier_curve(image,[(60, 57),(51, 47),(42,56),(35, 70)],2)

flood_fill1(image, 56, 42, 2,2)

bezier_curve(image,[(120, 128),(118, 123),(135, 101),(126,70)],2)
bezier_curve(image,[(110, 126),(130, 101),(126,70)],2)
flood_fill1(image, 117, 119, 2,2)

bezier_curve(image,[(126, 75),(130, 67),(142, 70),(150,86)],2)
bezier_curve(image,[(128, 65),(140, 60),(148, 68),(150,86)],2)

bezier_curve(image,[(128, 65),(140, 53),(150, 65), (159, 71)],2)
bezier_curve(image,[(130, 58),(143, 48),(153, 58),(159, 71)],2)

bezier_curve(image,[(130, 58),(132, 48),(138, 48)],2)
bezier_curve(image,[(126, 56),(126, 50),(132, 44),(138, 48)],2)

bezier_curve(image,[(125, 56),(120, 43),(105, 50)],2)
bezier_curve(image,[(121, 60),(117, 50),(105, 50)],2)

bezier_curve(image,[(121, 60),(105, 48),(93, 68)],2)
bezier_curve(image,[(120, 70),(115, 56),(93, 68)],2)

bezier_curve(image,[(120, 70),(114, 64),(106, 69),(100,84)],2)
bezier_curve(image,[(126, 75),(117, 70),(105, 78),(100,84)],2)

flood_fill1(image, 124, 60, 2, 2)

# Вывод рисунка
plt.imshow(image, cmap=cmap)
plt.axis('off')
plt.title("Тропический закат ")
plt.show()
