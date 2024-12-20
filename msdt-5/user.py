import random
import json
import time
from typing import List, Dict

class UserDataFetcher:
    """
    Класс для получения и обработки данных пользователя из API.
    """
    def __init__(self, api_url: str):
        self.api_url = api_url
    
    def fetch_data(self) -> Dict:
        """
        Получает данные с API и возвращает в виде словаря.
        """
        import requests
        response = requests.get(self.api_url)
        
        if response.status_code != 200:
            raise Exception("Failed to fetch data")
        
        return response.json()

    def process_data(self, data: Dict) -> Dict:
        """
        Преобразует и фильтрует данные для дальнейшей работы.
        """
        if "name" not in data or "age" not in data:
            raise ValueError("Invalid data format")
        
        return {
            "name": data["name"].upper(),
            "age": data["age"] * 2  # Увеличиваем возраст для примера
        }

class User:
    """
    Класс, представляющий пользователя с возможностью хранения и изменения его данных.
    """
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def update_info(self, new_name: str, new_age: int):
        self.name = new_name
        self.age = new_age

    def get_info(self) -> Dict:
        """
        Возвращает информацию о пользователе.
        """
        return {
            "name": self.name,
            "age": self.age
        }

    def is_adult(self) -> bool:
        """
        Проверка на совершеннолетие (возраст > 18).
        """
        return self.age >= 18

class Calculator:
    """
    Класс для выполнения базовых математических операций.
    """
    def add(self, a: int, b: int) -> int:
        return a + b

    def subtract(self, a: int, b: int) -> int:
        return a - b

    def multiply(self, a: int, b: int) -> int:
        return a * b

    def divide(self, a: int, b: int) -> float:
        if b == 0:
            raise ValueError("Division by zero")
        return a / b

class Database:
    """
    Симуляция базы данных для хранения пользователей.
    """
    def __init__(self):
        self.users = {}

    def add_user(self, user_id: str, user: User):
        self.users[user_id] = user

    def get_user(self, user_id: str) -> User:
        if user_id not in self.users:
            raise KeyError(f"User with id {user_id} not found")
        return self.users[user_id]

    def remove_user(self, user_id: str):
        if user_id in self.users:
            del self.users[user_id]
        else:
            raise KeyError(f"User with id {user_id} not found")

class RandomDataGenerator:
    """
    Класс для генерации случайных данных, например, для тестирования.
    """
    @staticmethod
    def generate_random_user() -> User:
        name = random.choice(["John", "Jane", "Alice", "Bob", "Charlie"])
        age = random.randint(18, 99)
        return User(name, age)

    @staticmethod
    def generate_random_number() -> int:
        return random.randint(1, 100)

class Timer:
    """
    Класс для замера времени выполнения операций.
    """
    def __init__(self):
        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self) -> float:
        if self.start_time is None:
            raise RuntimeError("Timer was not started")
        return time.time() - self.start_time

def save_to_file(data: Dict, filename: str):
    """
    Сохраняет данные в файл в формате JSON.
    """
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_from_file(filename: str) -> Dict:
    """
    Загружает данные из файла в формате JSON.
    """
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise Exception(f"File {filename} not found")
