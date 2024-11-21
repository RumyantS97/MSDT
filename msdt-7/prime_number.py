from asyncio import TaskGroup
import math

numbers = [173189, 1200000, 12344000]


async def is_prime(number: int):
    for i in range(3, math.ceil(math.sqrt(number)) + 1):
        if number % i == 0:
            print('False')
            return
    print('True')


async def task2():
    async with TaskGroup() as group:
        for number in numbers:
            group.create_task(is_prime(number))
