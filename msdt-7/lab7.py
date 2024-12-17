import asyncio
import aiohttp
import random
import time
from aiohttp import ClientSession
from datetime import datetime

# Список серверов для проверки
SERVERS = [
    "http://example.com",
    "http://httpbin.org/status/200",
    "http://httpbin.org/status/500",
    "http://nonexistentwebsite.xyz",
]

# Псевдослучайные логи для имитации серверных логов
LOGS = [
    "INFO: Server started",
    "ERROR: Unable to connect to database",
    "INFO: Request processed successfully",
    "ERROR: Timeout error occurred",
    "INFO: Server shut down",
    "WARNING: High memory usage detected",
]


# Асинхронная функция для проверки доступности серверов
async def check_server_status(session: ClientSession, url: str) -> dict:
    try:
        async with session.get(url) as response:
            status = response.status
            return {"url": url, "status": status}
    except Exception as e:
        return {"url": url, "status": f"Error: {e}"}


# Асинхронная функция для имитации проверки логов на сервере
async def check_server_logs(server_name: str) -> dict:
    await asyncio.sleep(random.uniform(0.5, 2))  # Симулируем задержку
    log = random.choice(LOGS)
    return {"server": server_name, "log": log}


# Асинхронная функция для периодической проверки состояния сервера
async def monitor_servers(session: ClientSession, servers: list) -> list:
    tasks = [check_server_status(session, server) for server in servers]
    results = await asyncio.gather(*tasks)
    return results


# Генерация отчета о статусе серверов
async def generate_server_report(servers: list):
    async with aiohttp.ClientSession() as session:
        print(f"\nНачало мониторинга серверов: {datetime.now()}")
        status_results = await monitor_servers(session, servers)
        for result in status_results:
            print(f"Сервер: {result['url']} - Статус: {result['status']}")


# Асинхронная функция для асинхронной обработки логов на разных серверах
async def monitor_logs_on_servers(servers: list):
    tasks = [check_server_logs(server) for server in servers]
    log_results = await asyncio.gather(*tasks)
    for log_result in log_results:
        print(f"Лог для {log_result['server']}: {log_result['log']}")


# Главная асинхронная функция
async def main():
    print("Программа мониторинга серверов запущена...")

    # Создание списка серверов для проверки логов
    servers = [f"Server_{i}" for i in range(1, 6)]  # Пример 5 серверов

    # Параллельное выполнение задач мониторинга
    await asyncio.gather(
        generate_server_report(SERVERS),
        monitor_logs_on_servers(servers),
    )
    print("\nМониторинг завершен!")


# Запуск программы
if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())  # Запускаем главную асинхронную задачу
    print(f"\nПрограмма завершена. Время работы: {time.time() - start_time:.2f} секунд.")
