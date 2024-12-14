import os

#Функция вывода информации по лабораторной работе
def task():
    print("Лабораторная работа №3")
    print("Вариант №3. Выполнил студент группы 6102-020302D Васильев А.Л.")
    print("Задание:")
    print("    В исходном текстовом файле записаны строки, содержащие произвольные алфавитно-цифровые символы.")
    print("Требуется написать программу, которая для каждой строки исходного файла будет составлять и выводить")
    print("в результирующий файл слово из тех букв английского алфавита, которые не встречаются во входных данных")
    print("ни как строчные, ни как прописные, причём буквы должны идти в алфавитном порядке. Каждая буква должна")
    print("быть распечатана один раз. Буквы построенного слова должны быть прописными. Если во входных данных")
    print("встречаются все буквы английского алфавита, то следует вывести строчными буквами слово \"no\".")
    print("\n    Например, пусть в одной из строк исходного файла содержатся следующие символы:")
    print("absCDKLMNOPvwXYabcprst")
    print("    В этом случае в результирующем файле должно быть:")
    print("EFGHIJQUZ")
    print("")

#Функция для чтения файлов и записи в них
def file_processing(fInput, fOutput):
    fI = open(fInput, "r")
    fO = open(fOutput, "w")
    information = fI.readlines()
    for inS in  information:
        resultS = ""
        if inS != "\n":
            inS = inS.upper()
            resultS = string_processing(inS)
        fO.write(resultS + "\n")
    fI.close()
    fO.close()

#Функция для обработки строк исходного файла
def string_processing(s):
   res = ""
   for i in range(57, 47, -1):
       if s.find(chr(i)) != -1:
           res += chr(i)
   if res == "":
       res = "-1"
   return res

#Функция main

task()

flagIn = True
while flagIn:
    print("\nВведите имя исходного текстого файла для его обработки:")
    fileInput = input("Имя файла: ")
    if (os.path.exists(fileInput)):
        flagIn = False
        flagOut = True
        while flagOut:
            print("\nВведите имя результирующего текстого файла для его обработки:")
            fileOutput = input("Имя файла: ")
            if (os.path.exists(fileOutput)):
                flagOut = False
                file_processing(fileInput, fileOutput)
                print("\nКонец работы программы!")
            else:
                print("Ошибка ввода! Попробуйте снова!")
    else:
        print("Ошибка ввода! Попробуйте снова!")