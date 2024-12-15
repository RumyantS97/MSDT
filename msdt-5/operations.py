import math

class Operations:
    # Класс с различными математическими операциями

    def factorial(self, n):
        #Возвращает факториал числа n.
        if n < 0:
            raise ValueError("Невозможно определить факториал от отрицательного числа!")
        return math.factorial(n)

    def power(self, a, b):
        #Возвращает a в степени b.
        return a ** b

    def logarithm(self, a, b=math.e):
        #Возвращает логарифм числа a по основанию b.
        if a <= 0:
            raise ValueError("Невозможно определить логарифм для неположительных значений!")
        return math.log(a, b)

    def square_root(self, a):
        #Возвращает корень числа. 
        if a < 0:
            raise ValueError("Невозможно вычислить квадратный корень из отрицательного числа!")
        return math.sqrt(a)

    def division_by_modulus(self, a, b):
        #Возвращает остаток от деления a на b. 
        if b == 0:
            raise ZeroDivisionError("На ноль делить нельзя!")
        return a % b
