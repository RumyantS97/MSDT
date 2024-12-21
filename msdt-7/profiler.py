import cProfile
import memory_profiler
import sympy as sp
from LR7 import matrix_operations, calculate_integral, calculate_derivative, complex_number_operations

# Пример данных
A = [[1, 2] * 1000] * 1000  # Увеличиваем размер матрицы
B = [[5, 6] * 1000] * 1000
x = sp.symbols('x')
func = sp.sin(x)

@memory_profiler.profile
def main():
    # Профилирование операций с матрицами
    print("Операции с матрицами:")
    matrix_operations(A, B)

    # Профилирование интеграла
    print("Вычисление интеграла:")
    calculate_integral(func, x, 0, sp.pi)

    # Профилирование производной
    print("Вычисление производной:")
    calculate_derivative(func, x)

    # Профилирование комплексных чисел
    z1 = 2 + 3j
    z2 = 1 - 1j
    print("Операции с комплексными числами:")
    complex_number_operations(z1, z2)

if __name__ == "__main__":
    cProfile.run('main()')
