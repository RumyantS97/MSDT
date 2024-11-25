import asyncio
import random


async def fetch_data(name: str) -> str:
    """
    Simulates data fetching for a given task.

    :param name: Name of the task (e.g., "A", "B", "C").
    :return: The name of the task after data fetching is complete.
    """
    print(f"Начинаю загрузку данных для задачи {name}...")
    await asyncio.sleep(random.uniform(1, 3))  # Симуляция времени загрузки
    print(f"Загрузка данных для задачи {name} завершена!")
    return name  # Возвращаем название задачи


async def process_data(name: str) -> str:
    """
    Simulates data processing for a given task.

    :param name: Name of the task for which data is being processed.
    :return: The result of the data processing.
    """
    print(f"Начинаю обработку данных для задачи {name}...")
    await asyncio.sleep(random.uniform(1, 2))  # Симуляция времени обработки
    print(f"Обработка данных для задачи {name} завершена!")
    return f"Результат обработки данных для задачи {name}"


async def main() -> None:
    """
    The main asynchronous function that manages data fetching and processing.

    Creates asynchronous tasks for fetching data, waits for their completion,
    and then processes the fetched data concurrently.
    """
    tasks: list[asyncio.Task] = []
    names: list[str] = ["A", "B", "C"]  # Имена задач

    # Создаем задачи на загрузку данных
    for name in names:
        task = asyncio.create_task(fetch_data(name))
        tasks.append(task)

    fetched_names: list[str] = await asyncio.gather(*tasks)

    # Создаем задачи на обработку данных
    process_tasks: list[asyncio.Task] = [asyncio.create_task(process_data(name))
                                         for name in fetched_names
                                         ]
    results: list[str] = await asyncio.gather(*process_tasks)

    print("\nРезультаты:")
    for result in results:
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
