import math


class Calculator:
    # Калькулятор с базовыми операциями

    def add(self, a, b):
        self._validate_input(a, b)
        return a + b
    

    def subtract(self, a, b):
        self._validate_input(a, b)
        return a - b
    

    def multiply(self, a, b):
        self._validate_input(a, b)
        return a * b
    

    def divide(self, a, b):
        self._validate_input(a, b)
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b
    

    def sqrt(self, a):
        if not isinstance(a, (int, float)):
            raise TypeError("Input must be int or float")
        if a < 0:
            raise ValueError("Cannot calculate the square root of a negative number")
        return math.sqrt(a)
    

    @staticmethod
    def _validate_input(a, b):
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Inputs must be int or float")