from timeout_for_fractal_optimal_depth import calculate_optimal_depth
from structured_concurrency.structured_concurrency_test import get_image_list
from asyncio import run

async def main1():
    print(await calculate_optimal_depth(6, 100, -2.2, 1.2, -1.2, 1.2, 500, 500))

async def main2():
    print(len(await get_image_list()))

run(main2())