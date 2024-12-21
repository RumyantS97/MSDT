import cProfile
import memory_profiler
import numpy as np
import sympy as sp


# Оптимизированные функции
def optimized_matrix_operations(A, B):
    """Оптимизированные операции с матрицами."""
    A = np.array(A)
    B = np.array(B)

    addition = np.add(A, B)
    subtraction = np.subtract(A, B)
    multiplication = np.matmul(A, B)  # Используем matmul для более эффективного умножения
    transpose_A = np.transpose(A)
    transpose_B = np.transpose(B)

    return {
        "Сложение": addition,
        "Вычитание": subtraction,
        "Умножение": multiplication,
        "Транспонирование A": transpose_A,
        "Транспонирование B": transpose_B
    }


def calculate_integral(func, var, a, b):
    """Вычисление определенного интеграла."""
    integral = sp.integrate(func, (var, a, b))
    return integral


def calculate_derivative(func, var):
    """Вычисление производной."""
    derivative = sp.diff(func, var)
    return derivative


def complex_number_operations(z1, z2):
    """Операции с комплексными числами."""
    addition = z1 + z2
    subtraction = z1 - z2
    multiplication = z1 * z2
    division = z1 / z2

    return {
        "Сложение": addition,
        "Вычитание": subtraction,
        "Умножение": multiplication,
        "Деление": division
    }
if __name__ == "__main__":
    # Пример операций с матрицами
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    print("Операции с матрицами:", optimized_matrix_operations(A, B))

    # Пример вычисления интеграла
    x = sp.symbols('x')
    func = sp.sin(x)
    integral_result = calculate_integral(func, x, 0, sp.pi)
    print("Определенный интеграл sin(x) от 0 до π:", integral_result)

    # Пример вычисления производной
    derivative_result = calculate_derivative(func, x)
    print("Производная sin(x):", derivative_result)

    # Пример операций с комплексными числами
    z1 = 2 + 3j
    z2 = 1 - 1j
    print("Операции с комплексными числами:", complex_number_operations(z1, z2))