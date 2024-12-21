import asyncio
import aiohttp

async def fetch_weather(session, city):
    """Получает данные о погоде для указанного города."""
    api_key = "243939fbaecc49f4bbd130700240904"
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {"key": api_key, "q": city, "aqi": "no"}

    async with session.get(base_url, params=params) as response:
        if response.status == 200:
            data = await response.json()
            print(f"Погода в {city}: {data['current']['temp_c']}°C, "
                  f"{data['current']['condition']['text']}")
        else:
            print(f"Не удалось получить данные для {city}. "
                  f"Статус: {response.status}")

async def fetch_weather_for_cities():
    """Получает данные о погоде для списка городов."""
    cities = ["Москва", "Лондон", "Париж", "Нью-Йорк", "Токио"]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_weather(session, city) for city in cities]
        await asyncio.gather(*tasks)

async def periodic_weather_updates(interval, stop_event):
    """Периодически обновляет данные о погоде."""
    while not stop_event.is_set():
        print("Обновление данных о погоде...")
        await fetch_weather_for_cities()
        await asyncio.sleep(interval)

async def main():
    """Главная точка входа в приложение."""
    stop_event = asyncio.Event()

    # Запуск периодических обновлений погоды
    periodic_task_coro = periodic_weather_updates(60, stop_event)  # Обновление каждые 60 секунд
    asyncio.create_task(periodic_task_coro)

    # Имитация работы основной программы
    try:
        print("Программа работает. Нажмите Ctrl+C для остановки.")
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Остановка программы...")
        stop_event.set()

# Точка входа в программу
if __name__ == "__main__":
    asyncio.run(main())
