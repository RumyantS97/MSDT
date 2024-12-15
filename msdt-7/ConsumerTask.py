import asyncio

class ConsumerTask:
    def __init__(self, mediator, name):
        self.mediator = mediator
        self.name = name

    async def run(self):
        mult = 100000
        length = self.mediator.length() * mult

        for i in range(length):
            if i % mult == 0:
                number = self.mediator.get_number_units(i // mult)
                print(f"\033[31m{self.name}\033[0m - Read: <{number}> from position <{i // mult}>")
                await asyncio.sleep(0)  # Асинхронная пауза
