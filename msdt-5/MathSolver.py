import math

class MathSolver:
    def solve_quadratic(self, a, b, c):
        """Решает квадратное уравнение ax^2 + bx + c = 0."""
        discriminant = b**2 - 4*a*c
        if discriminant > 0:
            root1 = (-b + math.sqrt(discriminant)) / (2 * a)
            root2 = (-b - math.sqrt(discriminant)) / (2 * a)
            return (root1, root2)
        elif discriminant == 0:
            root = -b / (2 * a)
            return (root,)
        else:
            return "Нет действительных корней"

    def factorial(self, n):
        """Вычисляет факториал числа n."""
        if n < 0:
            return "Факториал отрицательного числа не определен"
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result

    def solve_cubic(self, a, b, c, d):
        """Решает кубическое уравнение ax^3 + bx^2 + cx + d = 0."""
        if a == 0:
            return "Это не кубическое уравнение"
        
        # Метод Кардано для поиска корней
        f = ((3*c/a) - ((b**2)/(a**2))) / 3
        g = ((2*(b**3))/(a**3) - (9*b*c)/(a**2) + (27*d/a)) / 27
        h = (g**2)/4 + (f**3)/27
        
        if h > 0:
            r = -(g/2) + math.sqrt(h)
            s = r ** (1/3)
            t = -(g/2) - math.sqrt(h)
            u = t ** (1/3)
            root = (s + u) - (b/(3*a))
            return (root,)
        elif h == 0 and f == 0 and g == 0:
            root = - (b / (3 * a))
            return (root,)
        else:
            r = -(g/2) + math.sqrt(-h)
            s = r ** (1/3)
            t = -(g/2) - math.sqrt(-h)
            u = t ** (1/3)
            root1 = s + u - (b/(3*a))
            root2 = complex(-0.5*(s + u) - (b/(3*a)), (math.sqrt(3)/2)*(s - u))
            root3 = complex(-0.5*(s + u) - (b/(3*a)), -(math.sqrt(3)/2)*(s - u))
            return (root1, root2, root3)

    def modulus(self, x):
        """Вычисляет модуль числа x."""
        return abs(x)

    def square_root(self, x):
        """Вычисляет квадратный корень из x."""
        if x < 0:
            return "Квадратный корень из отрицательного числа не определен"
        return math.sqrt(x)

    def cotangent(self, angle):
        """Вычисляет котангенс угла в радианах."""
        if math.tan(angle) == 0:
            return "Котангенс не определен"
        return 1 / math.tan(angle)

    def tangent(self, angle):
        """Вычисляет тангенс угла в радианах."""
        return math.tan(angle)