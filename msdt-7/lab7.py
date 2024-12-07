import asyncio
import random


async def fetch_data(task_id):
    print(f"Task {task_id}: Starting data fetch...")
    # Имитация длительной операции с помощью sleep
    await asyncio.sleep(random.randint(1, 3))  # Случайная задержка от 1 до 3 секунд
    print(f"Task {task_id}: Data fetch complete!")
    return f"Data from task {task_id}"


async def main():
    tasks = []

    # Создаем несколько асинхронных задач
    for i in range(5):
        task = asyncio.create_task(fetch_data(i))
        tasks.append(task)

    # Ожидаем завершения всех задач
    results = await asyncio.gather(*tasks)

    # Выводим результаты
    for result in results:
        print(result)


# Запускаем главный асинхронный цикл
if __name__ == "__main__":
    asyncio.run(main())
