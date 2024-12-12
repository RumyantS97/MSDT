import asyncio
import aiohttp
import random
from datetime import datetime

# Список сайтов на пинг
websites = [
    "https://api.github.com",
    "https://www.python.org",
    "https://www.wikipedia.org",
    "https://www.stackoverflow.com",
    "https://www.reddit.com",
    "https://www.linkedin.com",
    "https://www.microsoft.com",
    "https://www.apple.com",
    "https://www.amazon.com",
    "https://www.netflix.com",
    "https://www.spotify.com"
]


# Симуляция работы базы данных
async def fetch_from_database(query: str):
    print(f"Fetching from database with query: {query}")
    await asyncio.sleep(random.uniform(1, 3))
    result = {"data": [random.randint(1, 100) for _ in range(5)]}
    print(f"Database query complete: {result}")
    return result


# Симуляция обработки данных
async def process_data(data):
    print(f"Processing data: {data}")
    await asyncio.sleep(random.uniform(1, 2))
    processed = [x * 2 for x in data]
    print(f"Data processed: {processed}")
    return processed


# Пинг сайта
async def ping_website(session, url):
    try:
        start_time = datetime.now()
        async with session.get(url) as response:
            status = response.status
            content_length = len(await response.text())
            duration = (datetime.now() - start_time).total_seconds()
            print(f"Pinged {url}: Status {status}, Content-Length {content_length}, Time {duration:.2f}s")
            return {
                "url": url,
                "status": status,
                "content_length": content_length,
                "time": duration
            }
    except Exception as e:
        print(f"Failed to ping {url}: {e}")
        return {"url": url, "error": str(e)}


# Симуляция фоновой периодической операции
async def periodic_task():
    while True:
        print(f"[{datetime.now()}] Running periodic task...")
        await asyncio.sleep(5)


async def main():
    print("Starting async operations...")

    # Старт фоновой операции
    periodic_task_future = asyncio.create_task(periodic_task())

    # Создание aiohttp-сессии
    async with aiohttp.ClientSession() as session:
        # Получение данных из базы данных
        database_future = fetch_from_database("SELECT * FROM table")

        # Пинг сайтов
        ping_futures = [ping_website(session, url) for url in websites]

        # Ожидание завершения всех задач
        database_result = await database_future
        ping_results = await asyncio.gather(*ping_futures)

        # Обработка результатов из базы данных
        processed_data = await process_data(database_result["data"])

        # Суммаризация результатов
        print("\nSummary of Operations:")
        print("Processed Database Data:", processed_data)
        print("Ping Results:", ping_results)

    # Отмена фоновой операции
    periodic_task_future.cancel()
    try:
        await periodic_task_future
    except asyncio.CancelledError:
        print("Periodic task cancelled.")

if __name__ == "__main__":
    asyncio.run(main())
