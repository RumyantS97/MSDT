import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Функция для генерации ключа из пароля пользователя
def generate_key(password):
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    return key, salt

# Функция для шифрования данных
def encrypt_data(data, password):
    # Генерация ключа и соли
    key, salt = generate_key(password)
    
    # Инициализация объекта шифратора
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Добавление padding к данным
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    # Шифрование данных
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    # Возвращаем зашифрованные данные вместе с солью и IV
    return salt + iv + encrypted_data

# Функция для расшифровки данных
def decrypt_data(encrypted_data, password):
    # Извлечение соли и IV из зашифрованных данных
    salt = encrypted_data[:16]
    iv = encrypted_data[16:32]
    encrypted_data = encrypted_data[32:]
    
    # Генерация ключа из пароля и соли
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    
    # Инициализация объекта дешифратора
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Расшифровка данных
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    
    # Удаление padding
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(decrypted_data) + unpadder.finalize()
    
    return data

# Основная функция программы
def main():
    print("Приветствую вас в программе шифрования!")
    while True:
        choice = input("\nВыберите действие:\n1. Зашифровать данные\n2. Расшифровать данные\n3. Выход\nВаш выбор: ")
        
        if choice == '1':
            plaintext = input("Введите текст для шифрования: ").encode()
            password = input("Введите пароль: ")
            
            encrypted_data = encrypt_data(plaintext, password)
            
            filename = "C:\lr\msdt-4\\test.txt"
            with open(filename, "wb") as file:
                file.write(encrypted_data)
                
            print(f"Данные успешно зашифрованы и сохранены в файле {filename}.")
        
        elif choice == '2':
            filename = input("Введите имя файла с зашифрованными данными: ")
            try:
                with open(filename, "rb") as file:
                    encrypted_data = file.read()
            except FileNotFoundError:
                print(f"Файл {filename} не найден.")
                continue
            
            password = input("Введите пароль: ")
            
            try:
                decrypted_data = decrypt_data(encrypted_data, password)
                print("Расшифрованный текст:", decrypted_data.decode())
            except ValueError:
                print("Неверный пароль или поврежденные данные.")
        
        elif choice == '3':
            break
        
        else:
            print("Неправильный ввод. Попробуйте еще раз.")

if __name__ == "__main__":
    main()