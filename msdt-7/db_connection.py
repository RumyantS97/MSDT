import aiomysql
import asyncio

queries = [
    'SELECT * FROM client;',
    'SELECT * FROM client WHERE card_id > 5;'
]


async def execute_query(query):
    connection = await aiomysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='project'
    )
    async with connection.cursor() as cur:
        await cur.execute(query)
        result = await cur.fetchone()
        print(result)
    connection.close()


async def task1():
    jobs = [execute_query(query) for query in queries]
    await asyncio.gather(*jobs)
