import os

class FileManager:

    # Создания менеджера
    def __init__( self ):

        # Здесь будет инициализация логирования
        print("init")

    # Чтение файла
    def Read_File( self, file_path, keyword ):

        # Чтение содержимого
        try:
            with open( file_path, 'r' ) as file:
                context = file.read()

            print(context)
            # Шифрование содержимого
            encrypted_text = self.Vigenere_Encrypt( context, keyword )
            print(encrypted_text)
            # Возврат текста
            return encrypted_text

        # При ошибке ничего не делаем
        except Exception as e:
            raise FileNotFoundError("No such file or directory") from e
            return None


    # Шифрование текста
    def Vigenere_Encrypt( self, text, keyword ):

        print(text)
        # Инициализируем стартовые переменные
        encrypted_text = []
        keyword_repeated = []
        keyword_length = len(keyword)

        # Повторяем ключ на всю длину текста
        for i in range(len(text)):
            keyword_repeated.append(keyword[i % keyword_length])

        # Шифруем текст
        for i in range(len(text)):

            # Если текущий символ - буква
            if text[i].isalpha():

                # Рассчитываем смещение
                shift = ord(keyword_repeated[i]) - ord('a')

                # Шифруем символ
                encryppted_char = chr((ord(text[i]) - ord('a') + shift) % 26 + ord('a'))
                encrypted_text.append(encryppted_char)

            # Иные символы не шифруем
            else:
                encrypted_text.append(text[i])

        # Возврящаем получившийся результат
        return ''.join(encrypted_text)


    # Запись зашифрованного текста
    def Write_File( self, file_path, text ):

        # Записываем текст в файл
        try:
            with open( file_path, 'w' ) as file:
                file.write(text)

        # В случае ошибки ничего не пишем
        except Exception as e:
            raise FileNotFoundError("No such file or directory") from e

    # Удаление исходного файла
    def Delete_File( self, file_path ):

        # Попытка удаления
        try:
            os.remove(file_path)

        # Ошибка удаления
        except Exception as e:
            raise FileNotFoundError("No such file or directory") from e

# Код использования программы шифрования
if __name__ == "__main__":

    # Менеджер файлов
    file_manager = FileManager()

    # Исходный файл и ключ
    input_file = input("Enter the name of the source file with the extension: ")
    keyword = input("Enter the code word: ")

    # Получение зашифрованного текста
    encrypted_text = file_manager.Read_File( input_file, keyword )

    # Запись в новый файл
    file_manager.Write_File( "output.txt", encrypted_text)

    # Удаление следов
    file_manager.Delete_File(input_file)
