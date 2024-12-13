import numpy as np, matplotlib.pyplot as plt
from scipy.integrate import quad, solve_ivp
from scipy.optimize import minimize
from scipy.stats import norm
class polynomial:
    def __init__(self,coefficients):
        """
        Инициализация многочлена.

        :param coefficients: Коэффициенты многочлена (от старшего к младшему)
        """
        self.coefficients=np.array(coefficients)

    def __add__(self,other):
        """Сложение двух многочленов."""
        new_coeffs=np.polyadd(self.coefficients,other.coefficients)
        return polynomial(new_coeffs)

    def __sub__(self,other):
        """Вычитание двух многочленов."""
        new_coeffs=np.polysub(self.coefficients,other.coefficients)
        return polynomial(new_coeffs)

    def __mul__(self,other):
        """Умножение двух многочленов."""
        new_coeffs=np.polymul(self.coefficients,other.coefficients)
        return polynomial(new_coeffs)

    def evaluate(self,x):
        """Вычисляет значение многочлена в точке x."""
        return np.polyval(self.coefficients,x)

    def derivative(self):
        """Вычисляет производную многочлена."""
        deriv_coeffs=np.polyder(self.coefficients)
        return polynomial(deriv_coeffs)

    def integral(self):
        """Вычисляет неопределенный интеграл многочлена."""
        integral_coeffs=np.polyint(self.coefficients)
        return polynomial(integral_coeffs)

    def roots(self):
        """Находит корни многочлена."""
        return np.roots(self.coefficients)
class numericalIntegration:
    @staticmethod
    def integrate(func,a,b):
        """
        Численное интегрирование функции func от a до b.

        :param func: Функция для интегрирования
        :param a: Нижний предел интегрирования
        :param b: Верхний предел интегрирования
        :return: Значение интеграла
        """

        result, _=quad(func,a,b)
        return result
class differentialEquationSolver:
    @staticmethod
    def solve_ode(ode_func,y0,t_span,t_eval=None):
        """
        Решает обыкновенное дифференциальное уравнение.

        :param ode_func: Функция правой части уравнения dy/dt = f(t, y)
        :param y0: Начальные условия
        :param t_span: Интервал времени (t0, tf)
        :param t_eval: Массив точек времени для оценки решения
        :return: Результат решения уравнения
        """

        solution=solve_ivp(ode_func,t_span,y0,t_eval=t_eval)
        return solution
class optimizer:
    @staticmethod
    def minimize_function(func,initial_guess):
        """
        Минимизирует функцию func с начальным приближением initial_guess.

        :param func: Функция для минимизации
        :param initial_guess: Начальное приближение
        :return: Результат минимизации
        """

        result=minimize(func,initial_guess)
        return result
class matrixOperations:
    def __init__(self,matrix):
        """
        Инициализация класса с матрицей.

        :param matrix: Двумерный массив или список списков
        """

        self.matrix=np.array(matrix)
def transpose(self):
    """Вычисляет транспонированную матрицу."""
    return self.matrix.T
def determinant(self):
    """Вычисляет определитель матрицы."""
    return np.linalg.det(self.matrix)
def inverse(self):
    """Вычисляет обратную матрицу."""

    if self.determinant()==0:
        raise ValueError("Обратная матрица не существует для данной матрицы.")

    return np.linalg.inv(self.matrix)
def eigenvalues_and_vectors(self):
    """Вычисляет собственные значения и собственные векторы."""
    return np.linalg.eig(self.matrix)
class statistics:
    @staticmethod
    def mean(data):
        """Вычисляет среднее значение."""
        return np.mean(data)

    @staticmethod
    def variance(data):
        """Вычисляет дисперсию."""
        return np.var(data)

    @staticmethod
    def standard_deviation(data):
        """Вычисляет стандартное отклонение."""
        return np.std(data)

    @staticmethod
    def median(data):
        """Вычисляет медиану."""
        return np.median(data)

    @staticmethod
    def mode(data):
        """Находит моду (значение с максимальной частотой)."""
        values, counts=np.unique(data,return_counts=True)
        max_count_index=np.argmax(counts)
        return values[max_count_index]
def square_of_sine(x):
    """Функция для вычисления sin^2(x)."""
    return np.sin(x)**2
def ode_function(t, y):
    _=t
    """Функция правой части ODE."""
    return -2*y+1
def plot_polynomial(poly, x_range=(-10, 10), num_points=1000):
    """Построить график многочлена."""
    x_vals=np.linspace(x_range[0], x_range[1], num_points)
    y_vals=poly.evaluate(x_vals)

    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, y_vals, label='Многочлен')
    plt.title('График многочлена')
    plt.xlabel('x')
    plt.ylabel('P(x)')
    plt.axhline(0, color='black', lw=0.5)
    plt.axvline(0, color='black', lw=0.5)
    plt.grid()
    plt.legend()
    plt.show()
def plot_ode_solution(solution):
    """Построить график решения ODE."""
    plt.figure(figsize=(10, 6))
    plt.plot(solution.t,solution.y[0],label='y(t)')
    plt.title('Решение ODE')
    plt.xlabel('t')
    plt.ylabel('y')
    plt.axhline(0,color='black',lw=0.5)
    plt.axvline(0,color='black',lw=0.5)
    plt.grid()
    plt.legend()
    plt.show()
def plot_statistics(data):
    """Построить гистограмму и график плотности вероятности."""

    # Гистограмма данных
    plt.figure(figsize=(10, 6))
    count, bins, ignored = plt.hist(data,
                                    30,
                                    density=True,
                                    alpha=0.5,
                                    color='g',
                                    edgecolor='black')

    # Плотность вероятности нормального распределения
    mu=statistics.mean(data)
    sigma=statistics.standard_deviation(data)
    best_fit_line=norm.pdf(bins, mu, sigma)
    plt.plot(bins,
             best_fit_line,
             'r--',
             linewidth=2)

    plt.title('Гистограмма и плотность вероятности')
    plt.xlabel('Значение')
    plt.ylabel('Частота')
    plt.axhline(0,color='black',lw=0.5)
    plt.axvline(0,color='black',lw=0.5)
    plt.grid()
    plt.show()
def main():
    # Примеры операций с многочленами
    print("Примеры операций с многочленами:")

    poly1=polynomial([1, -3, 2])  # x^2 - 3x + 2
    poly2=polynomial([1, 1])  # x + 1

    poly_sum=poly1+poly2
    poly_diff=poly1-poly2
    poly_prod=poly1*poly2

    print("Сумма многочленов:", poly_sum.coefficients)
    print("Разность многочленов:", poly_diff.coefficients)
    print("Произведение многочленов:", poly_prod.coefficients)

    # График первого многочлена

    plot_polynomial(poly1)

    # Численное интегрирование
    print("\nЧисленное интегрирование:")

    integral_value=numericalIntegration.integrate(square_of_sine,
                                                    0,
                                                    np.pi)

    print(f"Интеграл от sin^2(x) от 0 до π: {integral_value}")

    # Решение обыкновенного дифференциального уравнения

    print("\nРешение обыкновенного дифференциального уравнения:")

    y0 = [0]

    t_span = (0, 5)

    solution = differentialEquationSolver.solve_ode(
        ode_function,
        y0,
        t_span,
        t_eval=np.linspace(0,
                           5,
                           100))

    plot_ode_solution(solution)

    # Оптимизация функции
    print("\nОптимизация функции:")

    func_to_minimize=lambda x: (x - 3) ** 2 + 1

    initial_guess=[0]

    result = optimizer.minimize_function(func_to_minimize,
                                         initial_guess)
    print(f"Минимум достигнут в точке {result.x[0]} с значением {result.fun}")

    # Пример работы с матрицами

    print("\nРабота с матрицами:")

    matrix_a = [[4, 2], [3, 1]]

    matrix_operations=matrixOperations(matrix_a)

    print("Матрица A:")
    print(matrix_operations.matrix)

    print("Транспонированная матрица A:")
    print(transpose(matrix_operations))

    print("Определитель матрицы A:")
    print(determinant(matrix_operations))

    try:
        # Генерация случайных данных для статистики
        data = np.random.normal(loc=5.0,
                                scale=2.0,
                                size=1000)

        print("\nСтатистические вычисления:")
        print("Среднее:",statistics.mean(data))
        print("Дисперсия:",statistics.variance(data))
        print("Стандартное отклонение:",statistics.standard_deviation(data))
        print("Медиана:",statistics.median(data))
        print("Мода:",statistics.mode(data))

        plot_statistics(data)

    finally:
        print("Все вычисления произведены")
if __name__ == "__main__":
    main()
