from asyncio import TaskGroup, timeout, sleep
import cmath
from PIL import Image, ImageColor

class Complex:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: 'Complex'):
        return Complex(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Complex'):
        return Complex(self.x - other.x, self.y - other.y)

    def __mul__(self, other: 'Complex'):
        return Complex(self.x * other.x - self.y * other.y, self.x * other.y + self.y * other.x)

    def __truediv__(self, other: 'Complex'):
        denominator = other.x**2 + other.y**2
        return Complex((self.x * other.x + self.y * other.y) / denominator,
                       (other.x * self.y - self.x * other.y) / denominator)

    @property
    def modulo(self):
        return abs(complex(self.x, self.y)) # Используем встроенную функцию для модуля



def formula(Zk: Complex, Z0: Complex) -> Complex:
    return Zk * Zk * Zk * Zk + Z0


async def get_point_iterations(Z0: Complex, depth: int) -> int:
    if Z0.modulo > 2:
        return 0
    Zk = Z0
    iterationCount = 0
    while iterationCount < depth and Zk.modulo < 2:
        Zk = formula(Zk, Z0)
        iterationCount += 1
    return iterationCount


async def process_fractal(x0: int, x1: int, y0: int, y1: int, width: int, height: int, depth: int) -> Image.Image:
    image = Image.new("RGB", (width, height))
    pixels = image.load()

    for j in range(width):
        for i in range(height):
            point = Complex(
                x0 + (x1 - x0) * j / (width - 1),
                y0 + (y1 - y0) * i / (height - 1)
            )
            interactionCount = await get_point_iterations(point, depth)
            color_index = interactionCount % 6
            colors = {
                0: ImageColor.getrgb("red"),
                1: ImageColor.getrgb("yellow"),
                2: ImageColor.getrgb("green"),
                3: ImageColor.getrgb("blue"),
                4: ImageColor.getrgb("magenta"),
                5: ImageColor.getrgb("cyan"),
            }
            pixels[j, i] = colors.get(color_index, ImageColor.getrgb("black")) #Обработка отсутствующего ключа
    await sleep(0.001) # для возникновений CancellationException в случае отмены корутины, в конце вычисления оно вызовется, и если корутина была отменена по таймауту, то вызовется искоючение. Без этой строчки оно спокойно вернет результат, и оиждающая сверху функция его получит, несмотря на таймаут(так же можно вместо этого в той же )
    return image


async def process_fractal_with_cancellation(x0, x1, y0, y1, width, height, depth):
    async with TaskGroup() as tg:
        await tg.create_task(process_fractal(x0, x1, y0, y1, width, height, depth))

async def calculate_optimal_depth(time_limit, initial_depth, x0, x1, y0, y1, width, height):
    depth = initial_depth
    is_timed_out = True
    while is_timed_out:
        is_timed_out = True
        try:
            async with timeout(time_limit):
                await process_fractal_with_cancellation(x0, x1, y0, y1, width, height, depth)
                is_timed_out = False
                print("sussceeded " + str(depth))
        except Exception as e:
            print("timed out with " + str(depth) + "|" + str(e))
            is_timed_out = True
            depth //= 2
    return depth




## this is my own kotlin withTimeout, which can be stopped even if theres wrong suspending(no suspends, but time-consuming)
# suspend fun <R> myWithTimeoutOrNull(time: Long, block: suspend CoroutineScope.() -> R) : R? {
#     val cs = CoroutineScope(Dispatchers.Default)
#     val mainJob = cs.async { cs.async { block() }.await() } // if use one await, and block is cancelled, there can be no exception if wrong suspension and await in next try will still be working.
#     val stopper = cs.launch {
#         delay(time)
#         mainJob.cancel()
#     }
#     val res = try{
#         mainJob.await()
#     }
#     catch (e: Exception){
#         null
#     }
#     stopper.cancel()
#     return res
# }

#or we can create new function based in withTimeout()

# suspend fun <R> myWithTimeoutOrNull1(time: Long, block: suspend CoroutineScope.() -> R) : R? {
#     return withTimeoutOrNull(time){
#         val cs = CoroutineScope(Dispatchers.Default)
#         cs.async { block() }.await()
#     }
# }