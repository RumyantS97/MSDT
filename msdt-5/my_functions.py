
def add(a, b):
    """Возвращает сумму двух чисел."""
    return a + b

def subtract(a, b):
    """Возвращает разность двух чисел."""
    return a - b

def multiply(a, b):
    """Возвращает произведение двух чисел."""
    return a * b

def divide(a, b):
    """Возвращает частное двух чисел. Генерирует ошибку при делении на ноль."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

def square(n):
    """Возвращает квадрат числа."""
    return n * n

def greet(name):
    """Возвращает приветствие для заданного имени."""
    return f"Hello, {name}!"

def fetch_data(api_url):
    """Имитация функции, которая получает данные из API."""
    import requests
    response = requests.get(api_url)
    return response.json()
