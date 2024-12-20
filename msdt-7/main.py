import asyncio
import aiohttp
import random


# Класс для асинхронной загрузки данных из API
class ApiFetcher:
    def __init__(self, name):
        self.name = name


    async def fetch_data(self, url):
        print(f"{self.name}: Началась загрузка данных из {url}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        await asyncio.sleep(random.uniform(0.5, 1.0))
                        print(f"{self.name}: Успешно получены данные из {url}")
                        return data
                    else:
                        raise Exception(f"HTTP Error: {response.status}")

        except Exception as e:
            print(f"{self.name}: Ошибка при загрузке данных из {url} - {e}")
            return None


# Асинхронная функция для обработки нескольких API-запросов
async def fetch_multiple_apis(urls):
    fetcher = ApiFetcher("Fetcher")
    tasks = [fetcher.fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results


async def main():
    URLS = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3",
        "https://jsonplaceholder.typicode.com/posts/4",
        "https://jsonplaceholder.typicode.com/posts/5"
    ]
    
    data = await fetch_multiple_apis(URLS)
    print("\nПолученные данные:")
    for item in data:
        print(item)


if __name__ == "__main__":
    asyncio.run(main())
