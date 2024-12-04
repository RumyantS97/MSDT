import asyncio
import random

''' Класс, имитирующий транзакцию
Полагаем время на проведение коммита и отката случайным 
в промежутке 0.5 - 1 с'''
class Transaction:
    def __init__(self, name):
        self.name = name

    async def commit(self):
        await asyncio.sleep(random.uniform(0.5, 1.0))
        print(self.name + " завершена. COMMIT")

    async def rollback(self):
        await asyncio.sleep(random.uniform(0.5, 1.0))
        print(self.name + " отменена. ROLLBACK")


''' Имитация выполнения транзакции
Транзакция коммитится, если оба файла прочитаны без ошибки,
иначе - откатывается '''
async def execute_transaction(transaction):
    print(transaction.name + " запущена")

    try:
        await asyncio.gather(
            read_file("Файл 1", transaction),
            read_file("Файл 2", transaction)
        )

        await transaction.commit()

    except Exception as e:
        print(e)
        await transaction.rollback()


''' Имитация чтения файла
Время на чтение - случайное время от 0.5 до 2 с
Ошибка при чтении файла - случайная с вероятностью 0.3 '''
async def read_file(filename, transaction):
    await asyncio.sleep(random.uniform(0.5, 2.0))

    if random.random() < 0.3:
        raise Exception(f"{transaction.name}: ошибка при чтении {filename}")

    print(f"{transaction.name}: прочитан {filename}")


async def main():
    transaction1 = Transaction("Транзакция 1")
    transaction2 = Transaction("Транзакция 2")
    transaction3 = Transaction("Транзакция 3")
    await asyncio.gather(
        execute_transaction(transaction1),
        execute_transaction(transaction2),
        execute_transaction(transaction3)
    )


if __name__ == "__main__":
    asyncio.run(main())