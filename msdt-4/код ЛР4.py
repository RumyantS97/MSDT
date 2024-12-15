import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad, solve_ivp


class Polynomial:
    def __init__(self, coefficients):
        """Инициализация многочлена."""
        self.coefficients = np.array(coefficients)

    def add(self, other):
        """Сложение двух многочленов."""
        new_coeffs = np.polyadd(self.coefficients, other.coefficients)
        return Polynomial(new_coeffs)

    def subtract(self, other):
        """Вычитание двух многочленов."""
        new_coeffs = np.polysub(self.coefficients, other.coefficients)
        return Polynomial(new_coeffs)

    def multiply(self, other):
        """Умножение двух многочленов."""
        new_coeffs = np.polymul(self.coefficients, other.coefficients)
        return Polynomial(new_coeffs)

    def evaluate_at(self, x):
        """Вычисляет значение многочлена в точке x."""
        value = np.polyval(self.coefficients, x)
        return value


class NumericalIntegration:
    @staticmethod
    def integrate_function(func, a, b):
        """Численное интегрирование функции func от a до b."""
        result, _ = quad(func, a, b)
        return result


class DifferentialEquationSolver:
    @staticmethod
    def solve_ode(ode_func, y0, t_span):
        """Решает обыкновенное дифференциальное уравнение."""
        solution = solve_ivp(ode_func, t_span, y0)
        return solution


def add_square_of_sine(x):
    """Функция для вычисления sin^2(x)."""
    return np.sin(x) ** 2


def compute_ode_function(t, y):
    """Функция правой части ODE."""
    return -2 * y + 1


def plot_polynomial(poly):
    """Построить график многочлена."""
    x_vals = np.linspace(0, 1, 5)
    y_vals = poly.evaluate_at(x_vals)

    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, y_vals)
    plt.title('График многочлена')
    plt.xlabel('x')
    plt.ylabel('P(x)')
    plt.axhline(0, color='black', lw=0.5)
    plt.axvline(0, color='black', lw=0.5)
    plt.grid()
    plt.show()


def main():
    # Примеры операций с многочленами
    poly1 = Polynomial([1, -3, 2])  # x^2 - 3x + 2
    poly2 = Polynomial([1, 1])  # x + 1

    # Вывод значений многочленов
    print(f"Многочлен 1 (P1): {poly1.coefficients}")
    print(f"Многочлен 2 (P2): {poly2.coefficients}")

    poly_sum = poly1.add(poly2)
    poly_diff = poly1.subtract(poly2)

    print(f"Сумма (P1 + P2): {poly_sum.coefficients}")
    print(f"Разность (P1 - P2): {poly_diff.coefficients}")

    # График первого многочлена
    plot_polynomial(poly1)

    # Численное интегрирование
    integral_value = NumericalIntegration.integrate_function(add_square_of_sine,0,
                                                             np.pi)

    print(f"Значение интеграла от 0 до π: {integral_value}")

    # Решение обыкновенного дифференциального уравнения
    y0 = [0]
    t_span = (0, 5)
    solution = DifferentialEquationSolver.solve_ode(compute_ode_function,
                                                    y0,
                                                    t_span)

    # Вывод значений решения ОДУ
    print("Решение ОДУ:")
    print(f"Решения: {solution.y[0]}")

if __name__ == "__main__":
    main()
