import numpy as np
import sympy as sp


def matrix_operations(A, B):
    """Выполняет сложные операции с матрицами: сложение, вычитание, умножение и транспонирование."""
    A = np.array(A)
    B = np.array(B)

    addition = A + B
    subtraction = A - B
    multiplication = A @ B  # Матрица A умноженная на матрицу B
    transpose_A = A.T
    transpose_B = B.T

    return {
        "Сложение": addition,
        "Вычитание": subtraction,
        "Умножение": multiplication,
        "Транспонирование A": transpose_A,
        "Транспонирование B": transpose_B
    }


def calculate_integral(func, var, lower_limit, upper_limit):
    """Вычисляет определенный интеграл функции func по переменной var от lower_limit до upper_limit."""
    integral = sp.integrate(func, (var, lower_limit, upper_limit))
    return integral


def calculate_derivative(func, var):
    """Вычисляет производную функции func по переменной var."""
    derivative = sp.diff(func, var)
    return derivative


def complex_number_operations(z1, z2):
    """Выполняет операции с комплексными числами: сложение, вычитание, умножение и деление."""
    z1 = complex(z1)
    z2 = complex(z2)

    addition = z1 + z2
    subtraction = z1 - z2
    multiplication = z1 * z2
    division = z1 / z2 if z2 != 0 else "Деление на ноль невозможно"

    return {
        "Сложение": addition,
        "Вычитание": subtraction,
        "Умножение": multiplication,
        "Деление": division
    }


# Примеры использования функций
if __name__ == "__main__":
    # Пример операций с матрицами
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    print("Операции с матрицами:", matrix_operations(A, B))

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
