"""
Данный скрипт загружает фотографии по ссылкам из файла links.txt.
"""
import asyncio
import os
from pathlib import Path
from urllib.parse import urlparse

import aiohttp
from bs4 import BeautifulSoup

# Создаем папку для сохранения фотографий, если она не существует
SAVE_DIR = Path("photos")
SAVE_DIR.mkdir(exist_ok=True)

# Заголовки для имитации браузера
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124"
                  " Safari/537.36"
}


async def fetch_image_url(session, page_url):
    """
    Функция для загрузки страницы и поиска ссылки на изображение
    """
    try:
        async with session.get(page_url, headers=headers) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                image_tag = soup.find(
                    'meta',
                    property="og:image"
                )
                if image_tag and image_tag.get('content'):
                    return image_tag['content']
                else:
                    print(
                        f"Не удалось найти изображение на странице: {page_url}"
                    )
            else:
                print(
                    f"Ошибка загрузки страницы {page_url}, статус: {response.status}"
                )
    except Exception as e:
        print(f"Ошибка при обработке страницы {page_url}: {e}")
    return None


async def download_image(session, image_url, save_path):
    """
    Функция для загрузки изображения
    """
    try:
        async with session.get(image_url, headers=headers) as response:
            if response.status == 200:
                with open(save_path, 'wb') as f:
                    f.write(await response.read())
                print(f"Скачано: {image_url}")
            else:
                print(
                    f"Не удалось скачать: {image_url}, статус: {response.status}"
                )
    except Exception as e:
        print(f"Ошибка при загрузке {image_url}: {e}")


async def process_links(file_path):
    """
    Функция для обработки списка ссылок
    """
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]

    async with aiohttp.ClientSession() as session:
        tasks = []
        for page_url in urls:
            image_url = await fetch_image_url(
                session,
                page_url
            )
            if image_url:
                parsed_url = urlparse(image_url)
                file_name = os.path.basename(parsed_url.path)
                save_path = SAVE_DIR / file_name
                tasks.append(
                    download_image(
                        session,
                        image_url,
                        save_path
                    )
                )
            await asyncio.sleep(1)

        # Запускаем загрузку всех фотографий
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    file_path = "links.txt"  # Путь к файлу с ссылками

    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден.")
    else:
        asyncio.run(process_links(file_path))
