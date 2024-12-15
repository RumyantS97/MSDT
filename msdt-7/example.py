import asyncio
import random


# Симуляция бариста, который готовит напитки
async def prepare_drink(drink_name, preparation_time):
    print(f"Приготовление {drink_name} началось.")
    await asyncio.sleep(preparation_time)
    print(f"{drink_name} готов!")
    return drink_name


# Симуляция клиента, который делает заказ
async def customer_order(customer_id):
    drink = random.choice(["Капучино", "Латте", "Эспрессо", "Чай", "Мокко"])
    preparation_time = random.randint(1, 3)  # Время приготовления от 1 до 3 секунд
    print(f"Клиент {customer_id} заказал {drink}.")
    # Асинхронно готовим напиток
    result = await prepare_drink(drink, preparation_time)
    print(f"Клиент {customer_id} получил свой {result}.")


# Менеджер, который обрабатывает очередь клиентов
async def cafe_manager():
    print("Добро пожаловать в кафе!")
    # Асинхронно обслуживаем несколько клиентов
    tasks = []
    for i in range(1, 6):  # Моделируем 5 клиентов
        tasks.append(customer_order(i))

    # Ожидаем завершения всех заказов
    await asyncio.gather(*tasks)
    print("Все клиенты обслужены!")


# Главная асинхронная функция
async def main():
    # Запуск работы менеджера кафе
    await cafe_manager()


# Запуск асинхронного приложения
if __name__ == '__main__':
    asyncio.run(main())
