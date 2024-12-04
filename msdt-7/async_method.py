import asyncio
import aiohttp
import json

BASE_URL = "https://iss.moex.com/iss/engines/{engine}/markets/{market}/boards/{board}/securities.json"

# Асинхронная функция для получения данных с API
async def get_api_data(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            return await response.json()
        else:
            print(f"Ошибка при запросе данных: {response.status}")
            return None

# Метод для подсчета общего количества сделок
def calculate_total_trades(data):
    if not data or 'marketdata' not in data:
        print('Пустые данные API или отсутствует marketdata')
        return 0

    market_data = data['marketdata']['data']
    columns = data['marketdata']['columns']
    trades_index = columns.index('NUMTRADES') if 'NUMTRADES' in columns else -1
    if trades_index == -1:
        print('NUMTRADES не найден в columns')
        return 0

    total_trades = 0
    for entry in market_data:
        trades = entry[trades_index]
        if trades is not None:
            total_trades += int(trades)

    return total_trades

# Метод для обработки рынка
async def process_market(session, engine, market_name, boards):
    print(f'Обрабатываем рынок: {market_name}')

    total_trades = 0

    # Создаем список запросов для каждой доски
    tasks = [
        get_api_data(session, BASE_URL.replace('{engine}', engine).replace('{market}', market_name).replace('{board}', board))
        for board in boards
    ]

    # Выполняем все запросы параллельно
    results = await asyncio.gather(*tasks)

    # Обрабатываем результаты
    for api_data in results:
        if api_data is not None:
            total_trades += calculate_total_trades(api_data)

    print(f'Сделок на рынке {market_name}: {total_trades}')

    return {
        'totalTrades': total_trades,
    }

# Главный метод для обработки всех рынков
async def process_all_markets():
    async with aiohttp.ClientSession() as session:
        all_markets_data = {}

        all_markets_data['bonds'] = await process_market(session, 'stock', 'bonds', ['TQCB', 'TQOB'])
        all_markets_data['shares'] = await process_market(session, 'stock', 'shares', ['TQBR', 'TQTF'])
        all_markets_data['currency'] = await process_market(session, 'currency', 'selt', ['CETS'])
        all_markets_data['futures'] = await process_market(session, 'futures', 'forts', ['RFUD'])

        return all_markets_data


# Запуск главной асинхронной функции
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(process_all_markets())
