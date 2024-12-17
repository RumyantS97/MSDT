import asyncio
import aiohttp
from bs4 import BeautifulSoup

# Список URL-адресов для парсинга
URLS = [
    "https://ssau.ru/",
    "https://github.com",
    "https://vk.com",
]


# Асинхронная функция для парсинга одного сайта
async def fetch_and_parse(session, url):
    try:

        async with session.get(url) as response:

            if response.status == 200:

                html = await response.text()

                soup = BeautifulSoup(html, "html.parser")

                title = soup.title.string if soup.title else "No title"
                print(f"Title of {url}: {title}")
            else:
                print(f"Failed to fetch {url}: Status code {response.status}")
    except Exception as e:
        print(f"Error fetching {url}: {e}")


# Основная асинхронная функция
async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_and_parse(session, url) for url in URLS]

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
