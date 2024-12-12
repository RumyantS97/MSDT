import asyncio
import httpx

# Список URL-адресов, к которым будем делать запросы
urls = [
    'https://ssau.ru',
    'https://yandex.ru',
    'https://www.google.com',
    'https://www.wikipedia.org',
]


async def fetch(client, url):
    """Асинхронная функция для выполнения HTTP-запроса к указанному URL."""
    response = await client.get(url)
    return url, response.text


async def process_result(url, content):
    """Асинхронная функция для обработки результата запроса."""
    print(f"Processing content from {url}...")

    return url, content[:200]


async def save_to_file(url, content):
    """Асинхронная функция для сохранения результата в файл."""
    filename = f"{url.replace('https://', '').replace('/', '_').replace('www.', '')}.txt"
    with open(filename, 'w') as file:
        file.write(content)
    print(f"Saved content from {url} to {filename}")


async def main():
    """Основная асинхронная функция, которая управляет выполнением запросов."""
    async with httpx.AsyncClient() as client:
        fetch_tasks = [fetch(client, url) for url in urls]

        fetch_results = await asyncio.gather(*fetch_tasks)

        process_tasks = [process_result(url, content) for url, content in fetch_results]

        process_results = await asyncio.gather(*process_tasks)

        save_tasks = [save_to_file(url, content) for url, content in process_results]


        await asyncio.gather(*save_tasks)


asyncio.run(main())
