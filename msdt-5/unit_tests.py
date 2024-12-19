import pytest


class FibonacciRandomGenerator:
    def __init__(self, min_value, max_value, count):
        if not isinstance(min_value, (int, float)) or not isinstance(max_value, (int, float)):
            raise ValueError("Ошибка: введите числовые значения для диапазона")
        if not isinstance(count, int):
            raise ValueError("Ошибка: введите числовое значение для количества чисел")
        if count <= 0:
            raise ValueError("Ошибка: количество чисел должно быть положительным")
        if count > 1000000:
            raise ValueError("Ошибка: превышено допустимое количество чисел (до 1 000 000)")
        if min_value > max_value:
            raise ValueError("Ошибка: минимальное значение не может быть больше максимального")

        self.min_value = min_value
        self.max_value = max_value
        self.count = count

    def generate(self):
        fib_numbers = self.fibonacci(self.count + 2)  # +2 для получения нужного количества
        random_numbers = [
            (fib_numbers[i] % (self.max_value - self.min_value + 1)) + self.min_value
            for i in range(2, self.count + 2)
        ]
        return random_numbers

    @staticmethod
    def fibonacci(n):
        a, b = 0, 1
        fib_sequence = []
        for _ in range(n):
            fib_sequence.append(a)
            a, b = b, a + b
        return fib_sequence


# Тесты для FibonacciRandomGenerator
@pytest.mark.parametrize("min_value, max_value, count", [
    (1.1, 10.5, 5),
    (5, 5, 3),
    (-10, -1, 5)
])
def test_floating_point_and_special_ranges(min_value, max_value, count):
    generator = FibonacciRandomGenerator(min_value, max_value, count)
    random_numbers = generator.generate()
    assert len(random_numbers) == count
    assert all(min_value <= num <= max_value for num in random_numbers)


def test_generation_with_equal_bounds():
    generator = FibonacciRandomGenerator(5, 5, 3)
    random_numbers = generator.generate()
    assert all(num == 5 for num in random_numbers)
    assert len(random_numbers) == 3


def test_invalid_input_range():
    with pytest.raises(ValueError, match="Ошибка: введите числовые значения для диапазона"):
        FibonacciRandomGenerator("abc", 10, 5)


def test_large_number_generation():
    with pytest.raises(ValueError, match="Ошибка: превышено допустимое количество чисел"):
        FibonacciRandomGenerator(1, 10, 1000001)


def test_min_greater_than_max():
    with pytest.raises(ValueError, match="Ошибка: минимальное значение не может быть больше максимального"):
        FibonacciRandomGenerator(10, 5, 5)


def test_negative_range():
    generator = FibonacciRandomGenerator(-10, -1, 5)
    random_numbers = generator.generate()
    assert len(random_numbers) == 5
    assert all(-10 <= num <= -1 for num in random_numbers)


def test_non_numeric_count():
    with pytest.raises(ValueError, match="Ошибка: введите числовое значение для количества чисел"):
        FibonacciRandomGenerator(1, 10, "abc")


def test_successful_generation():
    generator = FibonacciRandomGenerator(1, 10, 5)
    random_numbers = generator.generate()
    assert len(random_numbers) == 5
    assert all(1 <= num <= 10 for num in random_numbers)


if __name__ == "__main__":
    pytest.main()
