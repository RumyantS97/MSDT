import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Button

# Генерация поверхности Тюка
def generate_tuyk_surface(R, petal_count, a_steps, b_steps):
    K = petal_count * 0.5
    a = np.linspace(0, np.pi, a_steps)
    b = np.linspace(0, 2 * np.pi, b_steps)
    a, b = np.meshgrid(a, b)

    x = R * np.sin(a) * np.cos(b) * (1 + 0.5 * np.abs(np.sin(K * b)))
    y = R * np.sin(a) * np.sin(b) * (1 + 0.5 * np.abs(np.sin(K * b)))
    z = R * np.cos(a)

    return x, y, z

# Каркасная визуализация с фиксированными границами осей
def plot_wireframe(ax, x, y, z):
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

# функция проецирования через матрицу
def apply_projection_matrix(x, y, z, alpha, beta):
    projection_matrix = np.array([
        [np.cos(alpha), np.sin(beta), 0, 0],
        [-np.sin(alpha) * np.cos(beta), np.cos(alpha) * np.cos(beta), np.sin(beta), 0],
        [np.sin(alpha) * np.sin(beta), -np.cos(alpha) * np.sin(beta), np.cos(beta), 0],
        [0, 0, 0, 1]
    ])
    coords = np.vstack((x.flatten(), y.flatten(), z.flatten(), np.ones_like(x.flatten())))
    transformed_coords = projection_matrix @ coords
    return (transformed_coords[0].reshape(x.shape), 
            transformed_coords[1].reshape(y.shape), 
            transformed_coords[2].reshape(z.shape))

# Применение матрицы преобразований
def apply_transformation(x, y, z, transformation_matrix):
    coords = np.vstack((x.flatten(), y.flatten(), z.flatten(), np.ones_like(x.flatten())))
    transformed_coords = transformation_matrix @ coords
    return (transformed_coords[0].reshape(x.shape), 
            transformed_coords[1].reshape(y.shape), 
            transformed_coords[2].reshape(z.shape))

# Матрица для трансляции
def translation_matrix(dx, dy, dz):
    return np.array([
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0, 1]
    ])

# Матрица для масштабирования
def scaling_matrix(factor):
    return np.array([
        [factor, 0, 0, 0],
        [0, factor, 0, 0],
        [0, 0, factor, 0],
        [0, 0, 0, 1]
    ])

# Матрица для вращения вокруг оси
def rotation_matrix(axis, angle):
    angle = np.radians(angle)
    if axis == 'x':
        return np.array([
            [1, 0, 0, 0],
            [0, np.cos(angle), -np.sin(angle), 0],
            [0, np.sin(angle), np.cos(angle), 0],
            [0, 0, 0, 1]
        ])
    elif axis == 'y':
        return np.array([
            [np.cos(angle), 0, np.sin(angle), 0],
            [0, 1, 0, 0],
            [-np.sin(angle), 0, np.cos(angle), 0],
            [0, 0, 0, 1]
        ])
    elif axis == 'z':
        return np.array([
            [np.cos(angle), -np.sin(angle), 0, 0],
            [np.sin(angle), np.cos(angle), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
    else:
        return np.eye(4)
# Обновление модели
def update_model(action, ax):
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

#обработка перемещения курсора
def on_mouse_move(event):
    last_mouse_position = (event.x, event.y)
    global alpha, beta
    if last_mouse_position is not None:
        dx = event.x - last_mouse_position[0]
        dy = event.y - last_mouse_position[1]
        alpha += np.radians(dx * 0.1)  
        beta += np.radians(dy * 0.1)  


# Интерфейс кнопок
def create_interface():
    root = Tk()
    root.title("3D Surface Transformations")

    # Создаём окно matplotlib
    global fig, ax
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    plot_wireframe(ax, x, y, z)  # Отображаем начальную модель
    plt.show(block=False)  # Запускаем окно графика

    # Подключаем фиктивный обработчик событий
    fig.canvas.mpl_connect("motion_notify_event", on_mouse_move)

    # Кнопки управления
    Button(root, text="Перемещение", command=lambda: update_model('translate', ax)).pack(pady=10)
    Button(root, text="Масштабирование", command=lambda: update_model('scale', ax)).pack(pady=10)
    Button(root, text="Вращение", command=lambda: update_model('rotate', ax)).pack(pady=10)

    root.mainloop()

# Параметры для генерации поверхности
R = 2.0  # Радиус
petal_count = 4  # Количество лепестков
a_steps = 30  # Количество шагов по a
b_steps = 30  # Количество шагов по b

alpha, beta = 0, 0
# Генерация исходной поверхности
x, y, z = generate_tuyk_surface(R, petal_count, a_steps, b_steps)

# Отображение интерфейса
create_interface()