import random
import time

class MyClass:
    def __init__(self):
        self.data = []
        self.name = "Test"
        self.size = 0

    def add_data(self, value):
        self.data.append(value)

    def get_data(self):
        return self.data

    def calc_sum(self, numbers):
        total = 0
        for num in numbers:
            total += num
        return total

    def calc_average(self, numbers):
        total = 0
        for num in numbers:
            total += num
        return total / len(numbers)

    def find_max(self, numbers):
        max_num = None
        for num in numbers:
            if max_num is None or num > max_num:
                max_num = num
        return max_num

    def find_min(self, numbers):
        min_num = None
        for num in numbers:
            if min_num is None or num < min_num:
                min_num = num
        return min_num

    def calc_square(self, numbers):
        result = []
        for num in numbers:
            result.append(num * num)
        return result

    def is_even(self, number):
        return number % 2 == 0

    def is_odd(self, number):
        return number % 2 != 0

    def check_even_odd(self, numbers):
        for number in numbers:
            if number % 2 == 0:
                print(f"{number} is even")
            else:
                print(f"{number} is odd")

    def generate_numbers(self, count):
        return [random.randint(1, 100) for _ in range(count)]

    def duplicate_check(self, numbers):
        seen = set()
        for num in numbers:
            if num in seen:
                print(f"Duplicate found: {num}")
            seen.add(num)

    def calc_total(self, numbers):
        return sum(numbers)

    def process_data(self, numbers):
        for num in numbers:
            if num % 2 == 0:
                print(f"Processing even number: {num}")
            else:
                print(f"Processing odd number: {num}")

    def simulate_time_delay(self):
        time.sleep(1)

    def find_duplicate_max(self, numbers):
        duplicates = []
        for num in numbers:
            if numbers.count(num) > 1 and num not in duplicates:
                duplicates.append(num)
        return duplicates

    def sort_numbers(self, numbers):
        return sorted(numbers)

    def reverse_sort_numbers(self, numbers):
        return sorted(numbers, reverse=True)

    def print_numbers(self, numbers):
        for num in numbers:
            print(f"Number: {num}")

    def remove_duplicates(self, numbers):
        return list(set(numbers))

    def process_data_advanced(self, numbers):
        for num in numbers:
            if num % 2 == 0:
                print(f"Advanced processing for even number: {num}")
            elif num % 3 == 0:
                print(f"Advanced processing for number divisible by 3: {num}")
            else:
                print(f"Processing for other number: {num}")

    def calculate_metrics(self, numbers):
        total = sum(numbers)
        average = total / len(numbers)
        max_num = max(numbers)
        min_num = min(numbers)
        return total, average, max_num, min_num

    def calculate_all(self, numbers):
        total = 0
        for num in numbers:
            total += num
        average = total / len(numbers)
        return total, average

    def perform_action(self, numbers):
        if len(numbers) > 5:
            print("Big list")
        else:
            print("Small list")
        print("Action performed")

    def find_middle_value(self, numbers):
        sorted_nums = sorted(numbers)
        mid = len(numbers) // 2
        if len(numbers) % 2 == 0:
            return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2
        else:
            return sorted_nums[mid]

    def process_multiple_times(self, numbers):
        for i in range(5):
            self.process_data(numbers)
            print(f"Round {i + 1} completed")

    def test_function(self, numbers):
        total = 0
        for num in numbers:
            total += num
        return total

    def combine_results(self, list1, list2):
        return list1 + list2

    def perform_complex_action(self, numbers):
        for num in numbers:
            if num % 2 == 0:
                print(f"Even: {num}")
            elif num % 3 == 0:
                print(f"Multiple of 3: {num}")
            else:
                print(f"Other: {num}")

    def process_numbers_and_print(self, numbers):
        for num in numbers:
            print(num)

    def process_and_calculate(self, numbers):
        total = sum(numbers)
        average = total / len(numbers)
        return total, average

    def check_and_process(self, numbers):
        for num in numbers:
            if num % 2 == 0:
                print(f"Even number: {num}")
            elif num % 5 == 0:
                print(f"Divisible by 5: {num}")
            else:
                print(f"Other number: {num}")

    def iterate_and_print(self, numbers):
        for num in numbers:
            print(f"Iterating: {num}")

    def print_summary(self, numbers):
        total = sum(numbers)
        average = total / len(numbers)
        print(f"Summary - Total: {total}, Average: {average}")

    def calculate_and_print(self, numbers):
        total = sum(numbers)
        print(f"Total: {total}")
        return total

    def check_duplicates(self, numbers):
        unique_numbers = set(numbers)
        if len(unique_numbers) < len(numbers):
            print("Duplicates found")
        else:
            print("No duplicates")

    def handle_time_delay(self):
        time.sleep(0.5)

    def process_and_compute(self, numbers):
        total = 0
        for num in numbers:
            total += num
        average = total / len(numbers)
        return total, average
