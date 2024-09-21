import os
def hello():
    print('''Лабораторнная работа №3
    Вариант №8. Выполнил студент группы 6103-020302D Красюк А. М.
    Задание: В исходном текстовом файле записаны строки, содержащие произвольные алфавитно-цифровые символы.  Требуется написать, которая для каждой строки исходного файла будет 
    составлять и выводить в результирующий файл слово из тех букв английского алфавита, которые встречаются во входных данных либо как строчные, либо как прописные, причем 
    буквы должны идти в алфавитном порядке. Каждая буква должна быть распечатана один раз. Буквы построенного слова должны быть прописными. Если во входных данных встречаются 
    все буквы английского алфавита, то следует вывести строчными буквами слово "no". Например, пусть в одной из строк исходного файла содержатся следующие символы:
    absCDKLMNOPvwXYabcprst. В этом случае в результирующем файле должно быть:
    ABCDKLMNOPRSTVWXY''')

def handler(line):
    string = ''
    for number in range(ord('A'), ord('Z') + 1):
        if chr(number) in line or chr(number + 32) in line:
            if not chr(number) in string:
                string += chr(number)
    if '\n' in line:
        string+='\n'
        if len(string)==27:
            string='no\n'
    else:
        if len(string) == 26:
            string = 'no'
    return string

def file_read(input_name, output_name):
    with open(input_name) as input_file:
        for line in input_file.readlines():
            string = handler(line)
            file_write(output_name, string)

def file_write(output_name, string):
    with open(output_name, 'a') as file:
        file.write(string)

hello()
input_name = input('Введите название исходного файла с расширением .txt\n')
output_name = input('Введите название результирующего файла с расширением .txt\n')
while not os.path.exists(input_name):
    input_name = input('Введите название файла корректно\n')
file_read(input_name, output_name)
print('Результат был записан в файл {0}'.format(output_name))