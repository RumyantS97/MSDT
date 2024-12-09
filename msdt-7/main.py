import aiohttp
import asyncio

# Ваш API ключ от OpenWeatherMap
API_KEY = 'd61d8f8dc28fa7930eaa3a2090956b19'


async def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['name'], data['main']['temp']
                else:
                    print(f'Failed to retrieve data for {city}. Status code: {response.status}')
                    print(f'Response text: {await response.text()}')
                    return city, None
        except aiohttp.ClientError as e:
            print(f'Network error while retrieving data for {city}: {e}')
            return city, None
        except Exception as e:
            print(f'Unexpected error while retrieving data for {city}: {e}')
            return city, None


async def main():
    cities = ['Moscow', 'Samara', 'Saratov', 'Balakovo', 'Volsk']
    tasks = [get_weather(city) for city in cities]

    # Запускаем все задачи параллельно
    results = await asyncio.gather(*tasks)

    for city, temp in results:
        if temp is not None:
            print(f'Temperature in {city}: {temp}°C')
        else:
            print(f'Failed to retrieve data for {city}')


# Запускаем асинхронную функцию main
asyncio.run(main())