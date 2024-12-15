import random
import asyncio

class ProducerTask:
    def __init__(self, mediator, name):
        self.mediator = mediator
        self.name = name

    async def run(self):
        mult = 100000
        length = self.mediator.length() * mult

        for i in range(length):
            if i % mult == 0:
                number = random.randint(1, 101)
                self.mediator.set_number_units(i // mult, number)
                print(f"\033[31m{self.name}\033[0m - Write: <{number}> to position <{i // mult}>")
                await asyncio.sleep(0)  # Асинхронная пауза