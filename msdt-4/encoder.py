import os
import logging

class FileManager:

    # Создания менеджера
    def __init__( self, log_file = "file_manager.log" ):
        
        # Настройка логирования
        logging.basicConfig(
            filename = log_file,
            level = logging.INFO,
            format = '%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info("FileManager initialized.")
    
    # Чтение файла
    def Read_File( self, file_path, keyword ):

        # Чтение содержимого
        try:
            with open( file_path, 'r' ) as file:
                context = file.read()
            logging.info(f'Read file: {file_path}')
            
            # Шифрование содержимого
            encrypted_text = self.Vigenere_Encrypt( context, keyword )
            logging.info(f'The content is encrypted: {file_path}')
            
            # Возврат текста
            return encrypted_text

        # При ошибке ничего не делаем
        except Exception as e:
            logging.error(f'Error reading file {file_name}: {e}')
            return None


    # Шифрование текста
    def Vigenere_Encrypt( self, text, keyword ):

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
            logging.info(f'Written to file: {file_path}')

        # В случае ошибки ничего не пишем
        except Exception as e:
            logging.error(f'Error writing to file {file_path}: {e}')

    # Удаление исходного файла
    def Delete_File( self, file_path ):
        
        # Попытка удаления
        try:
            os.remove(file_path)
            logging.info(f'Deleted file {file_path}')

        # Ошибка удаления
        except Exception as e:
            logging.error(f'Error deleting file {file_path}: {e}')

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
