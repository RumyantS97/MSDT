import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad, solve_ivp
import logging

# Настройка конфигурации логирования
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Polynomial:
    def __init__(self, coefficients):
        """Инициализация многочлена."""
        self.coefficients = np.array(coefficients)
        #Логируем инициализацию многочлена
        logging.debug(f"Создан многочлен с коэффициентами: {self.coefficients}")

    def add(self, other):
        """Сложение двух многочленов."""
        new_coeffs = np.polyadd(self.coefficients, other.coefficients)
        # Логируем сложение двух многочленов
        logging.info(f"Сложение многочленов: {self.coefficients} + {other.coefficients}")
        return Polynomial(new_coeffs)

    def subtract(self, other):
        """Вычитание двух многочленов."""
        new_coeffs = np.polysub(self.coefficients, other.coefficients)
        # Логируем вычитание двух многочленов
        logging.info(f"Вычитание многочленов: {self.coefficients} - {other.coefficients}")
        return Polynomial(new_coeffs)

    def multiply(self, other):
        """Умножение двух многочленов."""
        new_coeffs = np.polymul(self.coefficients, other.coefficients)
        # Логируем умножение двух многочленов
        logging.info(f"Умножение многочленов: {self.coefficients} * {other.coefficients}")
        return Polynomial(new_coeffs)

    def evaluate_at(self, x):
        """Вычисляет значение многочлена в точке x."""
        value = np.polyval(self.coefficients, x)
        #Логируем вычисление значение многочлена в точке x
        logging.debug(f"Вычисление P({x}) = {value}")
        return value


class NumericalIntegration:
    @staticmethod
    def integrate_function(func, a, b):
        """Численное интегрирование функции func от a до b."""
        result, _ = quad(func, a, b)
        #Логируем численное интегрирование
        logging.info(f"Интегрирование функции от {a} до {b}, результат: {result}")
        return result


class DifferentialEquationSolver:
    @staticmethod
    def solve_ode(ode_func, y0, t_span):
        """Решает обыкновенное дифференциальное уравнение."""
        logging.debug(f"Решение ОДУ с начальным условием {y0} на интервале {t_span}")
        solution = solve_ivp(ode_func, t_span, y0)

        if solution.success:
            #Логируем информацию об успешном решении
            logging.info("Успешное решение ОДУ.")
        else:
            #Логируем ошибку решения
            logging.error("Не удалось решить ОДУ.")
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
    #Логируем информацию о построении графика
    logging.info("Построен график многочлена.")


def main():
    #Логируем начало программы
    logging.info("Запуск приложения.")

    # Примеры операций с многочленами
    poly1 = Polynomial([1, -3, 2])  # x^2 - 3x + 2
    poly2 = Polynomial([1, 1])  # x + 1

    poly_sum = poly1.add(poly2)
    poly_diff = poly1.subtract(poly2)

    # График первого многочлена
    plot_polynomial(poly1)

    # Численное интегрирование
    integral_value = NumericalIntegration.integrate_function(add_square_of_sine,0,
                                                             np.pi)

    # Решение обыкновенного дифференциального уравнения
    y0 = [0]
    t_span = (0, 5)
    solution = DifferentialEquationSolver.solve_ode(compute_ode_function,
                                                    y0,
                                                    t_span)


if __name__ == "__main__":
    main()
