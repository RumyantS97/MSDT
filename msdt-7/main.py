import asyncio
import aiohttp
from bs4 import BeautifulSoup

# Список URL-адресов для парсинга
URLS = [
    "https://www.google.com/",
    "https://www.python.org",
    "https://www.wikipedia.org",
]

async def fetch_page(session, url):
    """
    Асинхронно загружает страницу по указанному URL.
    """
    try:
        async with session.get(url) as response:
            print(f"Загружаю {url}...")
            return await response.text()
    except aiohttp.ClientError as e:
        print(f"Ошибка при загрузке {url}: {e}")
        return None

def parse_page(url, html):
    """
    Парсит HTML-страницу и извлекает заголовок и список ссылок.
    """
    if not html:
        return None
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string.strip() if soup.title else "Нет заголовка"

    # Извлекаем все ссылки на странице
    links = []
    for a_tag in soup.find_all("a", href=True):
        links.append(a_tag["href"])

    return {
        "url": url,
        "title": title,
        "links": links,
    }

async def main():
    """
    Основная функция для запуска парсинга.
    """
    async with aiohttp.ClientSession() as session:
        # Создаем задачи для загрузки страниц
        tasks = [fetch_page(session, url) for url in URLS]
        # Ожидаем загрузки всех страниц
        pages = await asyncio.gather(*tasks)

        # Парсим каждую страницу
        for url, html in zip(URLS, pages):
            result = parse_page(url, html)
            if result:
                print(f"URL: {result['url']}")
                print(f"Заголовок: {result['title']}")
                print(f"Ссылки ({len(result['links'])}):")
                for link in result['links'][:10]:  # Показываем первые 10 ссылок
                    print(f"  - {link}")
                print("-" * 40)

# Запускаем программу
asyncio.run(main())
