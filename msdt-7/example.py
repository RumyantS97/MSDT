import asyncio
import random


# Асинхронная задача для "запроса данных" с задержкой
async def fetch_data(url):
    print(f"Fetching data from {url}...")
    # Симулируем задержку (например, HTTP запрос)
    await asyncio.sleep(random.uniform(1, 3))  # Задержка от 1 до 3 секунд
    return f"Data from {url}"


# Асинхронная задача для обработки данных
async def process_data(data):
    print(f"Processing {data}...")
    # Симулируем обработку данных
    await asyncio.sleep(random.uniform(1, 2))  # Задержка от 1 до 2 секунд
    return f"Processed {data}"


# Главная асинхронная функция
async def main():
    urls = ["https://example.com", "https://example.org", "https://example.net"]

    # Создание списка задач для получения данных
    fetch_tasks = [fetch_data(url) for url in urls]

    # Асинхронно собираем все результаты
    fetched_data = await asyncio.gather(*fetch_tasks)

    # Обработка данных
    process_tasks = [process_data(data) for data in fetched_data]

    # Асинхронно обрабатываем все данные
    processed_data = await asyncio.gather(*process_tasks)

    # Вывод результатов
    print("\nResults after processing:")
    for result in processed_data:
        print(result)


if __name__ == "__main__":
    # Запуск асинхронной программы
    asyncio.run(main())
