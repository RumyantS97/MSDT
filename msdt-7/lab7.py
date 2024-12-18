import asyncio
import random


async def fetch_data(source: str):
    print(f"Fetching data from {source}...")
    await asyncio.sleep(random.uniform(1, 3))  # Simulate variable network delay
    data = f"Data from {source}"
    print(f"Finished fetching from {source}")
    return data


async def process_data(data):
    print(f"Processing {data}...")
    await asyncio.sleep(random.uniform(1, 2))  # Simulate processing delay
    result = f"Processed {data}"
    print(f"Finished processing {data}")
    return result


async def save_results(result):
    print(f"Saving {result} to database...")
    await asyncio.sleep(random.uniform(0.5, 1.5))
    print(f"Saved {result} to database")


async def main():
    sources = ["Source A", "Source B", "Source C"]

    # Fetch data concurrently
    fetch_tasks = [fetch_data(source) for source in sources]
    raw_data = await asyncio.gather(*fetch_tasks)

    # Process and save data sequentially
    for data in raw_data:
        processed_data = await process_data(data)
        await save_results(processed_data)


if __name__ == "__main__":
    asyncio.run(main())
