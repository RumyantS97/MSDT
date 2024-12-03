import string

def shift_char(char, shift):
    """Сдвигает символ на указанное количество позиций."""
    if char in string.ascii_lowercase:
        start = ord('a')
        return chr(start + (ord(char) - start + shift) % 26)
    elif char in string.ascii_uppercase:
        start = ord('A')
        return chr(start + (ord(char) - start + shift) % 26)
    else:
        return char

def scramble_text(text, shift=1):
    """Шифрует текст, сдвигая каждый символ на shift позиций."""
    return ''.join(shift_char(char, shift) for char in text)

def scramble_file(input_path, output_path, shift=1):
    """Читает текст из входного файла, шифрует его и записывает в выходной файл."""
    with open(input_path, 'r', encoding='utf-8') as infile:
        text = infile.read()
    scrambled_text = scramble_text(text, shift)
    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(scrambled_text)
