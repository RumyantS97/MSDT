import aiohttp
import asyncio

URLS = [
    "https://vk.com",
    "https://www.youtube.com",
    "https://nonexistent.baddomain",
    "https://fakeurl.try",
    "https://github.com",
    "https://python.org"
]

SUCCESS_FILE = "success.txt"
FAILURE_FILE = "failures.txt"


async def fetch_url(session, url):
    try:
        async with session.get(url, timeout=5) as response:  # Таймаут запроса 5 секунд
            status = response.status
            if status == 200:
                print(f"[SUCCESS] {url} -> Status: {status}")
                return url, "success", status
            else:
                print(f"[FAILURE] {url} -> Status: {status}")
                return url, "failure", status
    except Exception as e:
        print(f"[ERROR] {url} -> {str(e)}")
        return url, "error", str(e)


async def process_urls(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

    async with asyncio.Lock():
        with open(SUCCESS_FILE, "w") as success_file, open(FAILURE_FILE, "w") as failure_file:
            for url, result, status in results:
                if result == "success":
                    success_file.write(f"{url} -> Status: {status}\n")
                else:
                    failure_file.write(f"{url} -> Error: {status}\n")
    print("Результаты записаны в файлы.")


async def main():
    print("Начинаем обработку URL...")
    await process_urls(URLS)
    print("Обработка завершена.")


if __name__ == "__main__":
    asyncio.run(main())
