import numpy as np
import matplotlib.pyplot as plt
import logging
from tkinter import Tk, Button

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='app.log', filemode='w')
logger = logging.getLogger(__name__)

# Генерация поверхности Тюка
def generate_tuyk_surface(R, petal_count, a_steps, b_steps):
    logger.info("Генерация поверхности Тюка началась")
    K = petal_count * 0.5
    a = np.linspace(0, np.pi, a_steps)
    b = np.linspace(0, 2 * np.pi, b_steps)
    a, b = np.meshgrid(a, b)

    x = R * np.sin(a) * np.cos(b) * (1 + 0.5 * np.abs(np.sin(K * b)))
    y = R * np.sin(a) * np.sin(b) * (1 + 0.5 * np.abs(np.sin(K * b)))
    z = R * np.cos(a)

    logger.info("Поверхность Тюка сгенерирована")
    return x, y, z

# Каркасная визуализация с фиксированными границами осей
def plot_wireframe(ax, x, y, z):
    logger.info("Отображение модели в режиме каркасной визуализации")
    ax.clear()  # Очищаем текущий график
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Wireframe Model")

    # Устанавливаем фиксированные границы осей
    ax.set_xlim(-5, 5)  # Диапазон для оси X
    ax.set_ylim(-5, 5)  # Диапазон для оси Y
    ax.set_zlim(-5, 5)  # Диапазон для оси Z

    # Рисуем каркас модели
    for i in range(x.shape[0] - 1):
        for j in range(y.shape[1] - 1):
            ax.plot([x[i, j], x[i+1, j]], [y[i, j], y[i+1, j]], [z[i, j], z[i+1, j]], color='b')
            ax.plot([x[i, j], x[i, j+1]], [y[i, j], y[i, j+1]], [z[i, j], z[i, j+1]], color='b')

    fig.canvas.draw()  # Обновляем содержимое окна
    logger.info("Каркасная модель обновлена")

# функция проецирования через матрицу
def apply_projection_matrix(x, y, z, alpha, beta):
    logger.info("Применение матрицы проекции")
    projection_matrix = np.array([
        [np.cos(alpha), np.sin(beta), 0, 0],
        [-np.sin(alpha) * np.cos(beta), np.cos(alpha) * np.cos(beta), np.sin(beta), 0],
        [np.sin(alpha) * np.sin(beta), -np.cos(alpha) * np.sin(beta), np.cos(beta), 0],
        [0, 0, 0, 1]
    ])
    coords = np.vstack((x.flatten(), y.flatten(), z.flatten(), np.ones_like(x.flatten())))
    transformed_coords = projection_matrix @ coords
    logger.info("Матрица проекции применена успешно")
    return (transformed_coords[0].reshape(x.shape), 
            transformed_coords[1].reshape(y.shape), 
            transformed_coords[2].reshape(z.shape))

# Применение матрицы преобразований
def apply_transformation(x, y, z, transformation_matrix):
    logger.info("Применение матрицы преобразования")
    coords = np.vstack((x.flatten(), y.flatten(), z.flatten(), np.ones_like(x.flatten())))
    transformed_coords = transformation_matrix @ coords
    logger.info("Матрица преобразования применена успешно")
    return (transformed_coords[0].reshape(x.shape), 
            transformed_coords[1].reshape(y.shape), 
            transformed_coords[2].reshape(z.shape))

# Матрица для трансляции
def translation_matrix(dx, dy, dz):
    logger.info(f"Создание матрицы трансляции: dx={dx}, dy={dy}, dz={dz}")
    return np.array([
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0, 1]
    ])

# Матрица для масштабирования
def scaling_matrix(factor):
    logger.info(f"Создание матрицы масштабирования с коэффициентом {factor}")
    return np.array([
        [factor, 0, 0, 0],
        [0, factor, 0, 0],
        [0, 0, factor, 0],
        [0, 0, 0, 1]
    ])

# Обновление модели
def update_model(action, ax):
    logger.info(f"Обновление модели: действие = {action}")
    global x, y, z
    if action == 'translate':
        transformation = translation_matrix(dx=1, dy=1, dz=1)  # Матрица трансляции
    elif action == 'scale':
        transformation = scaling_matrix(factor=2)  # Матрица масштабирования
    elif action == 'rotate':
        transformation = rotation_matrix(axis='y', angle=15)  # Матрица вращения вокруг оси Y
    else:
        transformation = np.eye(4)  # Единичная матрица (без изменений)
    
    x, y, z = apply_transformation(x, y, z, transformation)
    plot_wireframe(ax, x, y, z)
    logger.info(f"Модель обновлена: действие = {action}")

# Интерфейс кнопок
def create_interface():
    root = Tk()
    root.title("3D Surface Transformations")

    logger.info("Запуск интерфейса приложения")
    global fig, ax
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    plot_wireframe(ax, x, y, z)  # Отображаем начальную модель
    plt.show(block=False)  # Запускаем окно графика

    # Кнопки управления
    Button(root, text="Перемещение", command=lambda: update_model('translate', ax)).pack(pady=10)
    Button(root, text="Масштабирование", command=lambda: update_model('scale', ax)).pack(pady=10)
    Button(root, text="Вращение", command=lambda: update_model('rotate', ax)).pack(pady=10)

    logger.info("Интерфейс приложения загружен")
    root.mainloop()

# Параметры для генерации поверхности
R = 2.0  # Радиус
petal_count = 4  # Количество лепестков
a_steps = 30  # Количество шагов по a
b_steps = 30  # Количество шагов по b

# Генерация исходной поверхности
logger.info("Инициализация генерации поверхности Тюка")
x, y, z = generate_tuyk_surface(R, petal_count, a_steps, b_steps)

# Отображение интерфейса
create_interface()
logger.info("Приложение завершило выполнение")