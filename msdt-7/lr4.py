import asyncio
import aiohttp  # Асинхронная библиотека для работы с HTTP

# Асинхронная функция для скачивания данных с URL
async def fetch_url(session, url):
    print(f"Начало скачивания: {url}")
    async with session.get(url) as response:
        content = await response.text()
        print(f"Завершено скачивание: {url}")
        return content

# Главная функция
async def main():
    urls = [
        "https://ssau.ru",
        "https://sergeybezrukov.ru/",
        "https://bilandima.ru/",
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

    # Вывод первых 100 символов скачанного содержимого
    for url, content in zip(urls, results):
        print(f"Контент с {url}: {content[:100]}...")

# Запуск программы
if __name__ == "__main__":
    asyncio.run(main())
