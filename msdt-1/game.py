import random

def welcome_message():
    print("Привет! Добро пожаловать в игру 'Угадай число'!")
    print("Я загадал число от 1 до 100, попробуй его угадать!")

def get_random_number():
    return random.randint(1, 100)

def get_user_input():
    while True:
        try:
            guess = int(input("Введи число: "))
            if 1 <= guess <= 100:
                return guess
            else:
                print("Пожалуйста, введите число от 1 до 100.")
        except ValueError:
            print("Ошибка! Введите корректное число.")

def check_guess(guess, number):
    if guess < number:
        print("Загаданное число больше.")
    elif guess > number:
        print("Загаданное число меньше.")
    else:
        print("Поздравляю! Ты угадал число!")
        return True
    return False

def play_game():
    number = get_random_number()
    attempts = 0
    guessed = False

    while not guessed:
        guess = get_user_input()
        attempts += 1
        guessed = check_guess(guess, number)
    print(f"Ты угадал число за {attempts} попыток!")

def play_again():
    while True:
        answer = input("Хочешь сыграть ещё раз? (да/нет): ").lower()
        if answer in ['да', 'yes']:
            return True
        elif answer in ['нет', 'no']:
            return False
        else:
            print("Пожалуйста, введите 'да' или 'нет'.")

def main():
    welcome_message()
    play_game()

    while play_again():
        print("Начинаем новую игру!")
        play_game()
    print("Спасибо за игру! До встречи!")

def count_attempts(attempts_list):#Подсчёт и вывод попыток угадать число
    if not attempts_list:
        print("Никто ещё не играл.")
    else:
        avg_attempts = sum(attempts_list) / len(attempts_list)
        print(f"Среднее количество попыток: {avg_attempts}")

def play_game_with_stats(): #Добавляем список для хранения количества попыток
    number = get_random_number()
    attempts = 0
    guessed = False
    attempts_list = []

    while not guessed:
        guess = get_user_input()
        attempts += 1
        guessed = check_guess(guess, number)
    attempts_list.append(attempts)
    print(f"Ты угадал число за {attempts} попыток!")
    count_attempts(attempts_list)


def main_with_stats():#Основная программа с выводом статистики
    welcome_message()
    play_game_with_stats()

    while play_again():
        print("Начинаем новую игру!")
        play_game_with_stats()
    print("Спасибо за игру! До встречи!")


def start_program():#Начало программы с выбором режима игры
    print("Выбери режим: 1 - со статистикой, 2 - простой режим")
    choice = int(input("Ваш выбор: "))
    if choice == 1:
        main_with_stats()
    elif choice == 2:
        main()


start_program()