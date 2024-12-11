import sys


def gcd(a, b):
    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a


def main(args):
    if len(args) != 2:
        print("Использование: python gcd.py x1 x2")
        return

    try:
        x1 = int(args[0])
        x2 = int(args[1])

        if x1 <= 0 or x2 <= 0:
            print("Ожидался ввод двух целых положительных чисел.")
            return

        print(f"Проверка чисел: {x1} и {x2} удовлетворяют условиям.")
        print("Производится вычисление...")
        result = gcd(x1, x2)
        print(f"НОД чисел {x1} и {x2} равен {result}")

    except ValueError:
        print("Ожидался ввод двух целых положительных чисел.")


if __name__ == "__main__":
    main(sys.argv[1:])
