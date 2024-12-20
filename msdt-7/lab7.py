import asyncio
import aiohttp


async def fetch(url):
    """Асинхронная функция для загрузки содержимого веб-страницы."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def main(urls):
    """Основная асинхронная функция для загрузки данных из списка URL."""
    tasks = []

    for url in urls:
        tasks.append(fetch(url))

    # Ожидание завершения всех задач
    results = await asyncio.gather(*tasks)

    for url, content in zip(urls, results):
        print(f'Content from {url} loaded with length: {len(content)}')


if __name__ == "__main__":
    # Список URL для загрузки
    urls = [
        'https://www.example.com',
        'https://www.python.org',
        'https://www.github.com',
        'https://www.wikipedia.org',
        'https://www.stackoverflow.com'
    ]

    # Запуск асинхронного приложения
    asyncio.run(main(urls))
