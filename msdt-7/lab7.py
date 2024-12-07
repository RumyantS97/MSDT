import asyncio
import random
import aiofiles
from datetime import datetime


class Task:
    """Класс для представления задачи."""

    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.status = 'Создана'
        self.result = None

    async def run(self):
        """Асинхронное выполнение задачи."""
        self.status = 'Выполняется'
        await asyncio.sleep(self.duration)  # Имитация выполнения задачи
        self.result = f'Результат задачи {self.name}'
        self.status = 'Завершена'


class TaskManager:
    """Класс для управления задачами."""

    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        """Добавление задачи в менеджер."""
        self.tasks.append(task)

    async def execute_tasks(self):
        """Асинхронное выполнение всех задач."""
        tasks = [task.run() for task in self.tasks]
        await asyncio.gather(*tasks)

    async def save_results(self, filename):
        """Сохранение результатов выполнения задач в файл."""
        async with aiofiles.open(filename, 'a') as f:
            for task in self.tasks:
                await f.write(f'{datetime.now()}: {task.name} - {task.status}, {task.result}\n')


async def main():
    """Главная функция приложения."""
    manager = TaskManager()

    # Создание задач с случайной продолжительностью
    for i in range(5):
        duration = random.randint(1, 5)
        task = Task(name=f'Задача {i + 1}', duration=duration)
        manager.add_task(task)

    print("Начало выполнения задач...")

    # Выполнение задач
    await manager.execute_tasks()

    # Сохранение результатов в файл
    await manager.save_results('task_results.txt')

    print("Все задачи выполнены и результаты сохранены.")


if __name__ == "__main__":
    asyncio.run(main())
