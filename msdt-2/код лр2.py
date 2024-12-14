import numpy as np, matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# Параметрическая функция для супертороида
def supertoroid( a,b,s,t,u,v ):
    """Функция создания параметрических координат супертороида."""
    cu=np.sign(np.cos(u)) * (abs(np.cos(u)) ** s)
    su=np.sign(np.sin(u)) * (abs(np.sin(u)) ** s)
    cv=np.sign(np.cos(v)) * (abs(np.cos(v)) ** t)
    sv=np.sign(np.sin(v)) * (abs(np.sin(v)) ** t)

    x =(a+cu)*cv
    y =(b+cu)*sv
    z = su
    return x, y, z


# Аксонометрическая проекция
def axonometricprojection( x, y, z, alpha=np.radians(0), beta=np.radians(0) ):
    """Применяем аксонометрическую проекцию к 3D-объекту."""
    xp = x*np.cos(alpha)+y*np.sin(alpha)
    yp = -x*np.sin(alpha)*np.cos(beta)+y*np.cos(alpha)*np.cos(beta)+z*np.sin(beta)
    zp = (x*np.sin(alpha)*np.sin(beta)-y
          *np.cos(alpha)*np.sin(beta)+z*np.cos(beta))
    return xp, yp, zp


# Аффинные преобразования через матрицы
def affinetransform( points, matrix ):
    """Применение аффинного преобразования к набору точек."""
    points_h = np.concatenate([points, np.ones((1, points.shape[1]))])  # Гомогенные координаты
    transformed_points = matrix @ points_h
    return transformed_points[:3]


def translationmatrix( dx, dy, dz ):
    """Создание матрицы сдвига."""
    return np.array([
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0, 1]
    ])


def scalingmatrix( sx, sy, sz ):
    """Создание матрицы масштабирования."""
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])


def rotationxmatrix( theta ):
    """Создание матрицы вращения вокруг оси X."""
    return np.array([
        [1, 0, 0, 0],
        [0, np.cos(theta), -np.sin(theta), 0],
        [0, np.sin(theta), np.cos(theta), 0],
        [0, 0, 0, 1]
    ])


def rotationymatrix( theta ):
    """Создание матрицы вращения вокруг оси Y."""
    return np.array([
        [np.cos(theta), 0, np.sin(theta), 0],
        [0, 1, 0, 0],
        [-np.sin(theta), 0, np.cos(theta), 0],
        [0, 0, 0, 1]
    ])


def rotationzmatrix(theta):
    """Создание матрицы вращения вокруг оси Z."""
    return np.array([
        [np.cos(theta), -np.sin(theta), 0, 0],
        [np.sin(theta), np.cos(theta), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])


# Создаём сетку параметров u и v
u = np.linspace(0, 2 * np.pi, 30)
v = np.linspace(0, 2 * np.pi, 30)
u, v = np.meshgrid(u, v)

# Исходный супертороид
a, b, s, t = 2,2,1,1
x, y, z = supertoroid(a, b, s, t, u, v)
points = np.array([x.flatten(), y.flatten(), z.flatten()])

# Аффинные преобразования
translated_points = affinetransform(points, translationmatrix(3, -4, 5))  # Сдвиг по X
scaled_points = affinetransform(points, scalingmatrix(1.5, 1.5, 1.5))    # Масштабирование
rotated_x_points = affinetransform(points, rotationxmatrix(np.radians(45)))  # Вращение по X
rotated_y_points = affinetransform(points, rotationymatrix(np.radians(45)))  # Вращение по Y
rotated_z_points = affinetransform(points, rotationzmatrix(np.radians(45)))  # Вращение по Z

# Настраиваем график
fig = plt.figure(figsize=(14, 8))

# Проекцию строим для каждого преобразования
datasets = [
    ("Исходный объект", points),
    ("Сдвиг вдоль осей", translated_points),
    ("Масштабирование", scaled_points),
    ("\nВращение вокруг X", rotated_x_points),
    ("\nВращение вокруг Y", rotated_y_points),
    ("\nВращение вокруг Z", rotated_z_points),
]

for i, (title, data) in enumerate(datasets):
    ax = fig.add_subplot(2, 3, i + 1, projection='3d')
    x, y, z = axonometricprojection(*data)
    x = x.reshape(u.shape)
    y = y.reshape(u.shape)
    z = z.reshape(u.shape)
    ax.plot_wireframe(x, y, z, color='black', linewidth=0.5)
    ax.set_title(title)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4,4)
    ax.set_zlim(-4,4)

plt.tight_layout()
plt.show()