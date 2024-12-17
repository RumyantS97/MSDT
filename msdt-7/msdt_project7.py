import asyncio
import logging
import random
import time

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Список городов
cities = ["Moscow", "New York", "London", "Tokyo", "Berlin", "Paris", "Sydney"]


# Эмуляция API погоды
async def fetch_weather_data(city: str) -> dict:
    """
    Асинхронная функция для имитации запроса данных о погоде для города.
    В реальной программе тут бы был запрос к реальному API.
    """
    # Имитация случайной задержки в запросе
    await asyncio.sleep(random.uniform(0.5, 2.0))

    # Симуляция успеха/неудачи в запросе
    if random.random() < 0.1:
        raise ValueError(f"Ошибка получения данных для города {city}")

    # Возвращение "случайныех данных о погоде
    return {
        "city": city,
        "temperature": random.randint(-10, 35),
        "condition": random.choice(["Sunny", "Cloudy", "Rainy", "Snowy"]),
    }


# Асинхронная функция для получения погоды для нескольких городов
async def get_weather_for_cities(cities: list) -> list:
    """
    Получает информацию о погоде для всех городов в списке с использованием асинхронных запросов.
    """
    tasks = []
    for city in cities:
        tasks.append(fetch_weather_data(city))

    # Ожидаение выполнения всех асинхронных задач
    results = await asyncio.gather(*tasks, return_exceptions=True)

    return results


# Обработка результатов и логирование
async def process_weather_data():
    """
    Основная асинхронная функция для получения и обработки данных погоды.
    """
    logging.info("Запрос данных о погоде начат...")

    start_time = time.time()
    weather_data = await get_weather_for_cities(cities)

    for result in weather_data:
        if isinstance(result, Exception):
            logging.error(f"Произошла ошибка: {result}")
        else:
            city = result["city"]
            temperature = result["temperature"]
            condition = result["condition"]
            logging.info(f"Погода в городе {city}: {temperature}°C, {condition}")

    logging.info(f"Запрос данных завершен. Время выполнения: {time.time() - start_time:.2f} секунд")


# Главная асинхронная функция программы
async def main():
    await process_weather_data()


# Запуск асинхронной программы
if __name__ == "__main__":
    asyncio.run(main())
