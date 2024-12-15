import asyncio
import json
import pandas as pd
from aiohttp import ClientSession


async def get_weather(city):
    # Начинаем сессию
    async with ClientSession() as session:
        
        # Определяем ID города
        city_id = get_city_id(city)
        if city_id == 0:
            return f'{city}: Информация не найдена'
        
        # Создаём URL
        url = f'http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid=946573469234fd45c62df88c17233820&lang=ru'
        # Посылаем запрос
        async with session.get(url=url) as response:
            
            # Получаем ответ
            weather = await response.json()
            # Вывод: "Город, температура, погода, влажность, скорость_ветра, направление_ветра"
            return [city, weather["main"]["temp"] - 273.15, weather["weather"][0]["main"], weather["main"]["humidity"], weather["wind"]["speed"], wind_direction(weather["wind"]["deg"])]


# Получение ID города для запроса
def get_city_id(name_city):
    global data
    # Ищем город в базе
    for city in data:
        if city["name"] == name_city:
            return city["id"]
    # Ошибка если не найден
    return 0

# Направление ветра
def wind_direction(corner):
    if (corner <= 11.25 or corner > 348.75): return "C"
    elif (corner > 11.25 and corner <= 33.75): return "С-С-В"
    elif (corner > 33.75 and corner <= 56.25): return "С-В"
    elif (corner > 56.25 and corner <= 78.75): return "В-С-В"
    elif (corner > 78.75 and corner <= 101.25): return "В"
    elif (corner > 101.25 and corner <= 123.75): return "В-Ю-В"
    elif (corner > 123.75 and corner <= 146.25): return "Ю-В"
    elif (corner > 146.25 and corner <= 168.75): return "Ю-Ю-В"
    elif (corner > 168.75 and corner <= 191.25): return "Ю"
    elif (corner > 191.25 and corner <= 213.75): return "Ю-Ю-З"
    elif (corner > 213.75 and corner <= 236.25): return "Ю-З"
    elif (corner > 236.25 and corner <= 258.75): return "З-Ю-З"
    elif (corner > 258.75 and corner <= 281.25): return "З"
    elif (corner > 281.25 and corner <= 303.75): return "З-С-З"
    elif (corner > 303.75 and corner <= 326.25): return "С-З"
    else: return "С-С-З"
        
# Вывод результатов в виде таблицы
def to_console(data):
    # Создаём DataFrame
    df = pd.DataFrame( data, columns = [ "Город", "Темп.", "Погода", "Влажн.", "Скорость ветра", "Напр. ветра" ])
    print(df)

async def main(cities_):
    
    # Список задач
    tasks = []

    # Запрос погоды
    for city in cities_:
        tasks.append(asyncio.create_task(get_weather(city)))

    # Формируем единый ответ
    results = await asyncio.gather(*tasks)

    # Вывод результата в консоль
    to_console(results)

    
# Загружаем города из базы
with open( "city.list.json", "r", encoding = "utf-8" ) as f:
    data = json.load(f)

# Список исследуемых городов
cities = [ 'Moscow', 'Saint Petersburg', 'Novosibirsk', 'Yekaterinburg', 'Kazan',
          'Krasnoyarsk', 'Nizhniy Novgorod', 'Chelyabinsk', 'Ufa', 'Samara', 'Rostov-na-Donu', 'Krasnodar' ]

asyncio.run(main(cities))
