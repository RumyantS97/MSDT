import asyncio
import aiohttp
import logging


logging.basicConfig(level=logging.INFO)

async def fetch_cat_image(session):
    """
    Асинхронная функция для получения случайной картинки кота.
    Эта функция делает асинхронный HTTP-запрос к API The Cat API для получения 
    случайного изображения кота и возвращает URL изображения.
    """
    url = "https://api.thecatapi.com/v1/images/search"
    try:
        async with session.get(url) as response:
            data = await response.json()
            if response.status == 200:
                return data[0]['url']
            else:
                logging.error(f"Failed to fetch cat image, status code: {response.status}")
                return None
    except Exception as e:
        logging.error(f"Error while fetching cat image: {e}")
        return None


async def fetch_multiple_cat_images(session, count):
    """
    Асинхронная функция для получения нескольких случайных котов.
    Эта функция создает несколько асинхронных задач для получения случайных 
    изображений котов и возвращает список URL изображений.
    """
    tasks = []
    for _ in range(count):
        tasks.append(fetch_cat_image(session))
    results = await asyncio.gather(*tasks)
    return [result for result in results if result is not None]  # Фильтрация пустых результатов


async def download_cat_image(url, image_number):
    """
    Асинхронная функция для скачивания изображения.
    Эта функция выполняет асинхронный запрос для скачивания изображения по
    заданному URL и сохраняет его в файл.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    with open(f"cat_image_{image_number}.jpg", 'wb') as file:
                        file.write(await response.read())
                        logging.info(f"Downloaded image {image_number}")
                else:
                    logging.warning(f"Failed to download image {image_number}, status code: {response.status}")
    except Exception as e:
        logging.error(f"Error downloading image {image_number}: {e}")


async def fetch_cat_info(session, image_url):
    """
    Асинхронная функция для получения информации о коте.
    Эта функция делает запрос к API The Cat API для получения дополнительной 
    информации о коте, например, категорию кота.
    """
    url = f"https://api.thecatapi.com/v1/images/{image_url.split('/')[-1].split('.')[0]}"
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data[0].get('categories', 'Unknown')
            else:
                logging.warning(f"Failed to fetch cat info for {image_url}, status code: {response.status}")
                return None
    except Exception as e:
        logging.error(f"Error fetching cat info for {image_url}: {e}")
        return None


async def main():
    """
    Эта функция инициализирует сессию aiohttp, получает случайные изображения 
    котов и скачивает их. Также извлекает информацию о котах.
    """
    async with aiohttp.ClientSession() as session:
        logging.info("Fetching random cat images...")
        
        cat_urls = await fetch_multiple_cat_images(session, 5)
        logging.info(f"Fetched {len(cat_urls)} cat images.")

        tasks = []
        for index, url in enumerate(cat_urls):
            tasks.append(download_cat_image(url, index + 1))
            tasks.append(fetch_cat_info(session, url))

        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
