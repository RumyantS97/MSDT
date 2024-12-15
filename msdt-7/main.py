import asyncio 
import aiohttp 
from aiofiles import open as aio_open 
from datetime import datetime 
from tqdm import tqdm 

class URLMonitor: 
    def __init__(self, urls, max_concurrent_requests=100, output_file="results.log"): 
        self.urls = urls 
        self.max_concurrent_requests = max_concurrent_requests 
        self.output_file = output_file 
        self.semaphore = asyncio.Semaphore(max_concurrent_requests) 
        self.progress_bar = tqdm(total=len(urls), desc="Checking URLs") 

    async def check_url(self, session, url): 
        async with self.semaphore:  
            try: 
                async with session.get(url, timeout=10) as response: 
                    status = response.status 
                    result = f"{datetime.now()} - {url} - {status}\n" 
            except Exception as e: 
                result = f"{datetime.now()} - {url} - ERROR: {e}\n" 
        return result 

    async def process_urls(self): 
        async with aiohttp.ClientSession() as session: 
            tasks = [self.check_url(session, url) for url in self.urls] 
            async for task in self.run_with_progress_bar(tasks): 
                await self.log_result(task) 

    async def run_with_progress_bar(self, tasks): 
        for task in asyncio.as_completed(tasks): 
            result = await task 
            self.progress_bar.update(1) 
            yield result 

    async def log_result(self, result): 
        async with aio_open(self.output_file, mode="a") as file: 
            await file.write(result)

    def run(self): 
        loop = asyncio.get_event_loop() 
        loop.run_until_complete(self.process_urls()) 
        self.progress_bar.close() 
        print(f"Results saved to {self.output_file}") 

if __name__ == "__main__": 

    urls_to_check = [ 
        "https://example.com", 
        "https://google.com", 
        "https://nonexistent.broken", 
        "https://stackoverflow.com", 
    ] 

    monitor = URLMonitor(urls=urls_to_check, max_concurrent_requests=5) 
    monitor.run()

