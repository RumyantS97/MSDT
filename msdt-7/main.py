import asyncio


async def read_file(file_name):
    print(f"Начато чтение файла: {file_name}")
    try:
        async with open(file_name, "r", encoding="utf-8") as file:
            content = await file.read()
            print(f"Содержимое файла {file_name}:\n{content}\n")
    except FileNotFoundError:
        print(f"Файл {file_name} не найден!")
    except Exception as e:
        print(f"Ошибка при чтении файла {file_name}: {e}")


async def main():
    files = ["file1.txt", "file2.txt", "file3.txt"]

    tasks = [read_file(file) for file in files]

    await asyncio.gather(*tasks)


asyncio.run(main())
