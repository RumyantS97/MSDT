import sys


def segment_replace(mas, a1, b1, a2, b2):
    a1 -= 1
    b1 -= 1
    a2 -= 1
    b2 -= 1
    if a1 >= b1 or a2 >= b2:
        raise Exception("Не удалось создать файл с результатом")
    if a1 not in range(len(mas)) or b1 not in range(len(mas)) or a2 not in range(len(mas)) or b2 not in range(len(mas)):
        raise Exception("Не удалось создать файл с результатом")
    if b1 - a1 != b2 - a2:
        raise Exception("Не удалось создать файл с результатом")
    if b1 >= a2 and b2 >= a1:
        raise Exception("Не удалось создать файл с результатом")
    for i in range(b1 - a1 + 1):
        mas[a1 + i], mas[a2 + i] = mas[a2 + i], mas[a1 + i]
    return mas


def main(args):
    if len(args) != 3:
        print("Неверные параметры ввода")
        return

    try:
        mas = list(map(int, args[0].split()))
        segment1 = args[1]
        segment2 = args[2]
    except:
        print("Неверные параметры ввода")
        return
    try:
        result = segment_replace(mas, segment1[0], segment1[1], segment2[0], segment2[1])
        print(f"Массив после перестановки сегментов: {result}")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main(sys.argv[1:])