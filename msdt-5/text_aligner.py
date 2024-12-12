import sys

def print_usage():
    print("Использование: python text_aligner.py InputFileName OutputFileName MaxWidth")
    sys.exit(1)

def align_text_right(input_file, output_file, max_width):
    if max_width <= 0 or max_width >= 200:
        raise ValueError("MaxWidth должен быть неотрицательным числом не более 200")

    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()

        if not lines:
            print("Файл пуст")
            sys.exit(1)

        aligned_lines = []

        for line in lines:
            stripped_line = line.rstrip()  
            if len(stripped_line) > max_width:
                stripped_line = stripped_line[:max_width] 
            aligned_line = stripped_line.rjust(max_width) 
            aligned_lines.append(aligned_line)

        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write("\n".join(aligned_lines))

        for aligned_line in aligned_lines:
            print(aligned_line)

        print("Текст успешно выровнен и записан в", output_file)

    except FileNotFoundError:
        print(f"Ошибка: файл {input_file} не найден")
        sys.exit(1)

    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 4:
        print_usage()

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    max_width = int(sys.argv[3])

    align_text_right(input_file, output_file, max_width)

if __name__ == "__main__":
    main()
