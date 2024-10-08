import random


def get_input(prompt, valid_responses):
    """Функция для получения и проверки ввода пользователя."""
    while True:
        response = input(prompt).strip().lower()
        if response in valid_responses:
            return response
        print("Некорректный ввод. Попробуйте еще раз.")


def room_one():
    print("Вы находитесь в комнате 1.")
    print("Здесь ничего нет.")
    move = get_input("Введите 'вперед', чтобы перейти в следующую комнату: ", ['вперед'])
    room_two()


def room_two():
    print("Вы находитесь в комнате 2.")
    print("На полу лежит старый меч.")
    action = get_input("Введите 'поднять', чтобы взять меч, "
                       "или 'вперед', чтобы двигаться дальше: ", ['поднять', 'вперед'])

    if action == "поднять":
        print("Вы подняли меч.")

    room_three()


def room_three():
    print("Вы находитесь в комнате 3.")
    print("Перед вами монстр!")
    action = get_input("Введите 'атака', чтобы сразиться с монстром, "
                       "или 'бег', чтобы убежать: ", ['атака', 'бег'])

    if action == "атака":
        fight_monster()
    else:
        print("Вы убежали обратно в комнату 2.")
        room_two()


def fight_monster():
    print("Начинается бой с монстром!")
    player_health = 100
    monster_health = 50
    while player_health > 0 and monster_health > 0:
        action = get_input("Введите 'удар', чтобы атаковать монстра, "
                           "или 'блок', чтобы защититься: ", ['удар', 'блок'])

        if action == "удар":
            damage = random.randint(5, 15)
            monster_health -= damage
            print(f"Вы нанесли {damage} урона монстру.")
        elif action == "блок":
            print("Вы заблокировали удар монстра.")

        if monster_health > 0:
            monster_damage = random.randint(5, 10)
            player_health -= monster_damage
            print(f"Монстр атакует! Вы потеряли {monster_damage} здоровья.")
        else:
            print("Вы победили монстра!")
            room_four()

    if player_health <= 0:
        print("Вы погибли. Игра окончена.")
        game_over()


def room_four():
    print("Вы находитесь в комнате 4.")
    print("Здесь пусто, но дверь впереди открыта.")
    move = get_input("Введите 'вперед', чтобы пройти дальше: ", ['вперед'])
    room_five()


def room_five():
    print("Вы находитесь в комнате 5.")
    print("Вы встретили мудреца.")
    action = get_input("Введите 'говорить', чтобы поговорить с мудрецом, "
                       "или 'вперед', чтобы двигаться дальше: ", ['говорить', 'вперед'])

    if action == "говорить":
        print("Мудрец сказал: 'Будь осторожен в следующей комнате.'")

    room_six()


def room_six():
    print("Вы находитесь в комнате 6.")
    print("Перед вами большой сундук.")
    action = get_input("Введите 'открыть', чтобы открыть сундук, "
                       "или 'вперед', чтобы пройти дальше: ", ['открыть', 'вперед'])

    if action == "открыть":
        print("В сундуке лежит золотая корона!")

    room_seven()


def room_seven():
    print("Вы находитесь в комнате 7.")
    print("Здесь очень темно.")
    move = get_input("Введите 'вперед', чтобы двигаться дальше: ", ['вперед'])
    room_eight()


def room_eight():
    print("Вы находитесь в комнате 8.")
    print("Перед вами огромный дракон!")
    action = get_input("Введите 'сразиться', чтобы атаковать дракона, "
                       "или 'бег', чтобы убежать: ", ['сразиться', 'бег'])

    if action == "сразиться":
        fight_dragon()
    else:
        print("Вы убежали обратно в комнату 7.")
        room_seven()


def fight_dragon():
    print("Начинается бой с драконом!")
    player_health = 100
    dragon_health = 200
    while player_health > 0 and dragon_health > 0:
        action = get_input("Введите 'удар', чтобы атаковать дракона, "
                           "или 'блок', чтобы защититься: ", ['удар', 'блок'])

        if action == "удар":
            damage = random.randint(10, 20)
            dragon_health -= damage
            print(f"Вы нанесли {damage} урона дракону.")
        elif action == "блок":
            print("Вы заблокировали огненный выдох дракона.")

        if dragon_health > 0:
            dragon_damage = random.randint(15, 30)
            player_health -= dragon_damage
            print(f"Дракон атакует! Вы потеряли {dragon_damage} здоровья.")
        else:
            print("Вы победили дракона!")
            print("Поздравляем! Вы прошли игру.")
            game_over()

    if player_health <= 0:
        print("Вы погибли. Игра окончена.")
        game_over()


def room_nine():
    print("Вы находитесь в комнате 9.")
    print("Здесь вы встречаете большого зомби!")
    action = get_input("Введите 'сразиться', чтобы сразиться с зомби, "
                       "или 'бег', чтобы убежать: ", ['сразиться', 'бег'])

    if action == "сразиться":
        fight_zombie()
    else:
        print("Вы убежали обратно в комнату 8.")
        room_eight()


def fight_zombie():
    print("Начинается бой с зомби!")
    player_health = 100
    zombie_health = 80
    while player_health > 0 and zombie_health > 0:
        action = get_input("Введите 'удар', чтобы атаковать зомби, "
                           "или 'блок', чтобы защититься: ", ['удар', 'блок'])

        if action == "удар":
            damage = random.randint(10, 20)
            zombie_health -= damage
            print(f"Вы нанесли {damage} урона зомби.")
        elif action == "блок":
            print("Вы заблокировали атаку зомби.")

        if zombie_health > 0:
            zombie_damage = random.randint(10, 20)
            player_health -= zombie_damage
            print(f"Зомби атакует! Вы потеряли {zombie_damage} здоровья.")
        else:
            print("Вы победили зомби!")
            room_ten()

    if player_health <= 0:
        print("Вы погибли. Игра окончена.")
        game_over()


def room_ten():
    print("Вы находитесь в комнате 10.")
    print("Здесь пусто, но впереди слышны шаги.")
    move = get_input("Введите 'вперед', чтобы продолжить игру: ", ['вперед'])
    room_eleven()


def room_eleven():
    print("Вы находитесь в комнате 11.")
    print("Здесь ничего нет.")
    move = get_input("Введите 'вперед', чтобы продолжить игру: ", ['вперед'])
    room_twelve()


def room_twelve():
    print("Вы находитесь в комнате 12.")
    print("Перед вами ещё один монстр!")
    action = get_input("Введите 'сразиться', чтобы атаковать монстра, "
                       "или 'бег', чтобы убежать: ", ['сразиться', 'бег'])

    if action == "сразиться":
        fight_monster_again()
    else:
        print("Вы убежали обратно в комнату 11.")
        room_eleven()


def fight_monster_again():
    print("Начинается бой с монстром!")
    player_health = 100
    monster_health = 60
    while player_health > 0 and monster_health > 0:
        action = get_input("Введите 'удар', чтобы атаковать монстра, "
                           "или 'блок', чтобы защититься: ", ['удар', 'блок'])

        if action == "удар":
            damage = random.randint(5, 15)
            monster_health -= damage
            print(f"Вы нанесли {damage} урона монстру.")
        elif action == "блок":
            print("Вы заблокировали удар монстра.")

        if monster_health > 0:
            monster_damage = random.randint(5, 10)
            player_health -= monster_damage
            print(f"Монстр атакует! Вы потеряли {monster_damage} здоровья.")
        else:
            print("Вы победили монстра!")
            room_thirteen()

    if player_health <= 0:
        print("Вы погибли. Игра окончена.")
        game_over()


def room_thirteen():
    print("Вы находитесь в комнате 13.")
    print("Вы нашли секретный выход!")
    print("Поздравляем, вы прошли игру.")
    game_over()


def game_over():
    print("Конец игры. Хотите сыграть снова?")
    replay = get_input("Введите 'да' для новой игры или 'нет', чтобы выйти: ", ['да', 'нет'])
    if replay == 'да':
        room_one()
    else:
        print("Спасибо за игру!")


def start_game():
    print("Добро пожаловать в текстовую игру!")
    room_one()


start_game()