import random
import math
import os


class FileProcessor:
    def __init__(self, filename):
        self.filename = filename

    def read_file(self):
        try:
            with open(self.filename, 'r') as file:
                content = [line.strip() for line in file.readlines()]
                return content
        except FileNotFoundError:
            print(f"File {self.filename} not found.")
            return []

    def write_random_numbers(self):
        try:
            with open(self.filename, 'w') as file:
                for _ in range(20):
                    file.write(f"{random.randint(1, 100)}\n")
        except Exception as e:
            print(f"Error writing to file: {e}")

    def delete_file(self):
        try:
            os.remove(self.filename)
        except FileNotFoundError:
            print(f"Tried to delete non-existent file {self.filename}.")


class MathOperations:
    def calculate_square_root(self, number):
        if number < 0:
            print("Attempted to calculate the square root of a negative number.")
            return None
        result = math.sqrt(number)
        print(f"Calculated square root of {number}: {result}")
        return result

    def find_gcd(self, a, b):
        result = math.gcd(a, b)
        print(f"Calculated GCD of {a} and {b}: {result}")
        return result

    def calculate_factorial(self, number):
        if number < 0:
            print("Attempted to calculate the factorial of a negative number.")
            return None
        result = math.factorial(number)
        print(f"Calculated factorial of {number}: {result}")
        return result


class InputHandler:
    def get_number_input(self):
        try:
            user_input = input("Enter a number: ")
            num = int(user_input)
            return num
        except ValueError:
            print("Invalid input. Not a number.")
            return None

    def get_operation_choice(self):
        print("Choose an operation:")
        print("1. Calculate Square Root")
        print("2. Calculate GCD")
        print("3. Calculate Factorial")
        try:
            choice = int(input("Enter your choice (1-3): "))
            if choice in [1, 2, 3]:
                return choice
            else:
                print("Invalid choice made.")
                return None
        except ValueError:
            print("Non-integer choice input.")
            return None


class TextProcessor:
    def get_user_text(self):
        user_text = input("Enter your text: ")
        return user_text

    def word_count(self, text):
        words = text.split()
        count = len(words)
        print(f"Word count: {count}")
        return count

    def find_longest_word(self, text):
        words = text.split()
        if not words:
            print("No words found in input text.")
            return None
        longest_word = max(words, key=len)
        print(f"Longest word: {longest_word}")
        return longest_word

    def reverse_text(self, text):
        reversed_text = text[::-1]
        print(f"Reversed text: {reversed_text}")
        return reversed_text


if __name__ == "__main__":
    # Работа с файлами
    processor = FileProcessor("numbers.txt")
    processor.write_random_numbers()
    content = processor.read_file()

    # Математические операции
    math_ops = MathOperations()

    # Обработка ввода
    handler = InputHandler()
    number = handler.get_number_input()

    operation = handler.get_operation_choice()
    if operation == 1:
        print(math_ops.calculate_square_root(number))
    elif operation == 2:
        print("Enter two numbers to find their GCD:")
        num1 = handler.get_number_input()
        num2 = handler.get_number_input()
        if num1 is not None and num2 is not None:
            gcd_result = math_ops.find_gcd(num1, num2)
            print(f"GCD of {num1} and {num2} is {gcd_result}")
        else:
            print("Invalid input for GCD calculation.")
    elif operation == 3:
        if number is not None:
            factorial_result = math_ops.calculate_factorial(number)
            if factorial_result is not None:
                print(f"Factorial of {number} is {factorial_result}")
            else:
                print("Invalid input for factorial calculation.")
    else:
        print("No valid operation selected.")

    # Обработка текста
    text_proc = TextProcessor()
    user_text = text_proc.get_user_text()
    word_count = text_proc.word_count(user_text)
    print(f"Word count of user input: {word_count}")

    longest_word = text_proc.find_longest_word(user_text)
    print(f"Longest word in user input: {longest_word}")

    reversed_text = text_proc.reverse_text(user_text)
    print(f"Reversed user input: {reversed_text}")

    # Завершение работы с файлом
    processor.delete_file()
