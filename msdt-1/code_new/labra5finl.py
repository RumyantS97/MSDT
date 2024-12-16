import pygame
import math
import numpy as np


class Visualizer:
    def __init__(self, width=800, height=800):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("3D")
        self.clock = pygame.time.Clock()

        self.scale = 1
        self.offset_x = width // 2
        self.offset_y = height // 2
        self.rotation = [0, 0, 0]

        # Создаем экземпляр класса Transform3D для работы с матрицами преобразований
        self.transformer = Transform3D()

        self.points = []
        self.lines = []

        self.generate_surface()
        self.buttons = self.create_buttons()

    def create_buttons(self):
        buttons = [
            {"text": "Влево", "action": lambda: self.transformer.translate(-50, 0, 0),
             "rect": pygame.Rect(10, 60, 60, 30)},
            {"text": "Вправо", "action": lambda: self.transformer.translate(50, 0, 0),
             "rect": pygame.Rect(10, 100, 60, 30)},
            {"text": "Вверх", "action": lambda: self.transformer.translate(0, -50, 0),
             "rect": pygame.Rect(10, 140, 60, 30)},
            {"text": "Вниз", "action": lambda: self.transformer.translate(0, 50, 0),
             "rect": pygame.Rect(10, 180, 60, 30)},
            {"text": "Масштаб +", "action": lambda: self.transformer.rescale(1.1),
             "rect": pygame.Rect(10, 220, 90, 30)},
            {"text": "Масштаб -", "action": lambda: self.transformer.rescale(0.9),
             "rect": pygame.Rect(10, 260, 90, 30)},
            {"text": "Вращение X", "action": lambda: self.transformer.rotate(10, 0, 0),
             "rect": pygame.Rect(10, 300, 90, 30)},
            {"text": "Вращение Y", "action": lambda: self.transformer.rotate(0, 10, 0),
             "rect": pygame.Rect(10, 340, 90, 30)},
            {"text": "Вращение Z", "action": lambda: self.transformer.rotate(0, 0, 10),
             "rect": pygame.Rect(10, 380, 90, 30)},
        ]
        return buttons

    def generate_surface(self):
        """Генерация точек и связей для поверхности."""
        self.points.clear()
        self.lines.clear()

        τ_values = np.linspace(0, 1.4 * math.pi, 50)
        θ_values = np.linspace(0, 1.5 * math.pi, 50)

        for i, τ in enumerate(τ_values):
            for j, θ in enumerate(θ_values):
                x = (1 + τ - np.sin(τ)) * np.cos(θ)
                y = 1 - np.cos(τ)
                z = -(1 + τ - np.sin(τ)) * np.sin(θ)
                self.points.append([x, y, z, 1])  # Добавляем w=1 для работы с матрицей

                if j > 0:
                    self.lines.append(((i * len(θ_values)) + j - 1, (i * len(θ_values)) + j))
                if i > 0:
                    self.lines.append((((i - 1) * len(θ_values)) + j, (i * len(θ_values)) + j))

    def transform(self, point):
        # Применяем трансформации (перемещение, масштабирование, вращение)
        transformed_point = self.transformer.transform_point(point)
        x, y, z = transformed_point

        # Отображаем по центру экрана
        x, y = x * self.scale + self.offset_x, y * self.scale + self.offset_y
        return x, y

    def render(self):
        self.screen.fill((255, 255, 255))  # Очищаем экран (фон белый)

        # Рисуем линии (синим цветом)
        for line in self.lines:
            p1 = self.transform(self.points[line[0]])
            p2 = self.transform(self.points[line[1]])

            pygame.draw.line(self.screen, (0, 0, 255), p1, p2)  # Синий цвет для линий

        # Рисуем кнопки 
        for button in self.buttons:
            pygame.draw.rect(self.screen, (200, 200, 200),
                             button["rect"])  # Цвет для кнопок
            font = pygame.font.SysFont('Verdana', 14)  # Шрифт кнопок
            text_surface = font.render(button["text"], True, (0, 0, 0))  # Цвет текста
            self.screen.blit(text_surface, (button["rect"].x + 5, button["rect"].y + 5))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button["rect"].collidepoint(pos):
                            button["action"]()

            self.render()
            self.clock.tick(30)

        pygame.quit()


class Transform3D:
    def __init__(self):
        self.model_matrix = np.eye(4)  # Единичная матрица 4x4
        self.translation_matrix = np.eye(4)  # Матрица для перемещения

    def translate(self, dx, dy, dz):
        translation_matrix = np.array([
            [1, 0, 0, dx],
            [0, 1, 0, dy],
            [0, 0, 1, dz],
            [0, 0, 0, 1]
        ])
        self.translation_matrix = translation_matrix @ self.translation_matrix

    def rescale(self, k):
        scaling_matrix = np.array([
            [k, 0, 0, 0],
            [0, k, 0, 0],
            [0, 0, k, 0],
            [0, 0, 0, 1]
        ])
        self.model_matrix = scaling_matrix @ self.model_matrix

    def rotate(self, dx, dy, dz):
        # Углы преобразуем в радианы
        rx, ry, rz = np.radians(dx), np.radians(dy), np.radians(dz)

        # Вращение вокруг X
        rotation_x = np.array([
            [1, 0, 0, 0],
            [0, np.cos(rx), -np.sin(rx), 0],
            [0, np.sin(rx), np.cos(rx), 0],
            [0, 0, 0, 1]
        ])

        # Вращение вокруг Y
        rotation_y = np.array([
            [np.cos(ry), 0, np.sin(ry), 0],
            [0, 1, 0, 0],
            [-np.sin(ry), 0, np.cos(ry), 0],
            [0, 0, 0, 1]
        ])

        # Вращение вокруг Z
        rotation_z = np.array([
            [np.cos(rz), -np.sin(rz), 0, 0],
            [np.sin(rz), np.cos(rz), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        # Объединяем вращения
        self.model_matrix = rotation_x @ rotation_y @ rotation_z @ self.model_matrix

    def transform_point(self, point):
        # Преобразование точки (добавляем координату w=1 для работы с 4x4 матрицей)
        point_4d = np.array([point[0], point[1], point[2], 1])

        # Применяем вращение, масштабирование и сдвиг
        transformed_point = self.model_matrix @ point_4d
        transformed_point = self.translation_matrix @ transformed_point

        # Применяем ортогональную проекцию (сбрасываем координату z)
        projection_matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 0],  # Ортогональная проекция, z = 0
            [0, 0, 0, 1]
        ])

        # Применяем проекцию
        projected_point = projection_matrix @ transformed_point

        return projected_point[:3]  # Возвращаем только x, y, z


# Запуск
visualizer = Visualizer()
visualizer.run()
