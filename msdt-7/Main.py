import asyncio
from Soldiers import Soldiers
from ProducerTask import ProducerTask
from ConsumerTask import ConsumerTask

async def main():
    while True:
        try:
            dimen = int(input("\nВведите размерность массива (количество баз): "))
            if dimen <= 0:
                raise ValueError("Размерность массива должна быть положительной!")
            break
        except ValueError as ex:
            print(f"\u001B[31mОшибка: {ex}\u001B[0m")

    mediator = Soldiers(num=dimen)

    while True:
        print("\nВыберите пункт из меню для продолжения работы:")
        print("\t1 - Запустить асинхронные задачи.")
        print("\t0 - Закончить работу.")

        choice = input("Ваш выбор: ")

        if choice == "0":
            print("\n\u001B[31mЗавершение работы!\u001B[0m")
            break

        producer_task = ProducerTask(mediator, "WriteTask")
        consumer_task = ConsumerTask(mediator, "ReadTask")

        # Запуск задач с использованием asyncio
        await asyncio.gather(
            producer_task.run(),
            consumer_task.run()
        )

if __name__ == "__main__":
    asyncio.run(main())
