
import math

class AdvancedMath:
    """Класс с продвинутыми математическими методами для работы с матрицами, векторами и численными методами."""

    # -------- Работа с векторами --------
    @staticmethod
    def vector_dot_product(v1, v2):
        """Скалярное произведение двух векторов."""
        if len(v1) != len(v2):
            raise ValueError("Vectors must have the same length")
        return sum(a * b for a, b in zip(v1, v2))

    @staticmethod
    def vector_magnitude(v):
        """Модуль (длина) вектора."""
        return math.sqrt(sum(x ** 2 for x in v))

    @staticmethod
    def vector_normalize(v):
        """Нормализация вектора."""
        magnitude = AdvancedMath.vector_magnitude(v)
        if magnitude == 0:
            raise ValueError("Cannot normalize a zero vector")
        return [x / magnitude for x in v]

    # -------- Работа с матрицами --------
    @staticmethod
    def matrix_addition(m1, m2):
        """Сложение двух матриц."""
        if len(m1) != len(m2) or len(m1[0]) != len(m2[0]):
            raise ValueError("Matrices must have the same dimensions")
        return [[m1[i][j] + m2[i][j] for j in range(len(m1[0]))] for i in range(len(m1))]

    @staticmethod
    def matrix_multiplication(m1, m2):
        """Умножение двух матриц."""
        if len(m1[0]) != len(m2):
            raise ValueError("Number of columns in first matrix must equal number of rows in second matrix")
        result = [
            [sum(m1[i][k] * m2[k][j] for k in range(len(m2))) for j in range(len(m2[0]))]
            for i in range(len(m1))
        ]
        return result

    @staticmethod
    def matrix_transpose(m):
        """Транспонирование матрицы."""
        return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]

    # -------- Численные методы --------
    @staticmethod
    def newton_raphson(f, df, x0, tolerance=1e-6, max_iterations=100):
        """
        Метод Ньютона-Рафсона для нахождения корня уравнения f(x) = 0.
        
        :param f: Функция
        :param df: Производная функции
        :param x0: Начальное приближение
        :param tolerance: Точность
        :param max_iterations: Максимальное количество итераций
        """
        x = x0
        for i in range(max_iterations):
            fx = f(x)
            dfx = df(x)
            if dfx == 0:
                raise ValueError("Derivative is zero. No solution found.")
            x_new = x - fx / dfx
            if abs(x_new - x) < tolerance:
                return x_new
            x = x_new
        raise ValueError("Newton-Raphson method did not converge")

    @staticmethod
    def integrate_trapezoidal(f, a, b, n=1000):
        """
        Численное интегрирование методом трапеций.
        
        :param f: Интегрируемая функция
        :param a: Нижний предел
        :param b: Верхний предел
        :param n: Количество разбиений
        """
        h = (b - a) / n
        integral = (f(a) + f(b)) / 2
        for i in range(1, n):
            integral += f(a + i * h)
        return integral * h