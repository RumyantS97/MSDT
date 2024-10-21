import random

def get_input(prompt, valid_responses):
    """
    Получает и проверяет ввод пользователя.

    :param prompt: Текстовый запрос для ввода.
    :param valid_responses: Список допустимых ответов.
    :return: Введенный пользователем ответ, если он корректный.
    """
    while True:
        response = input(prompt).strip().lower()
        if response in valid_responses:
            return response
        print("Некорректный ввод. Попробуйте еще раз.")

def room_one():
    """
    Обрабатывает события в первой комнате.
    Предлагает игроку двигаться вперед.
    """
    print("Вы находитесь в комнате 1.")
    print("Здесь ничего нет.")
    move = get_input("Введите 'вперед', чтобы перейти в следующую комнату: ", ['вперед'])
    if move == 'вперед':
        room_two()

def room_two():
    """
    Обрабатывает события во второй комнате.
    Игрок может взять меч или двигаться дальше.
    """
    print("Вы находитесь в комнате 2.")
    print("На полу лежит старый меч.")
    action = get_input("Введите 'поднять', чтобы взять меч, "
                       "или 'вперед', чтобы двигаться дальше: ", ['поднять', 'вперед'])
    if action == 'поднять':
        print("Вы подняли меч.")
    room_three()

def room_three():
    """
    Обрабатывает события в третьей комнате.
    Игрок сталкивается с монстром и может сражаться или убежать.
    """
    print("Вы находитесь в комнате 3.")
    print("Перед вами монстр!")
    action = get_input("Введите 'атака', чтобы сразиться с монстром, "
                       "или 'бег', чтобы убежать: ", ['атака', 'бег'])
    if action == 'атака':
        fight_monster()
    else:
        print("Вы убежали обратно в комнату 2.")
        room_two()

def fight_monster():
    """
    Запускает бой с монстром.
    Игрок и монстр обмениваются атаками, пока один не погибнет.
    """
    print("Начинается бой с монстром!")
    player_health = 100
    monster_health = 50
    while player_health > 0 and monster_health > 0:
        action = get_input("Введите 'удар', чтобы атаковать монстра, "
                           "или 'блок', чтобы защититься: ", ['удар', 'блок'])
        if action == 'удар':
            damage = random.randint(5, 15)
            monster_health -= damage
            print(f"Вы нанесли {damage} урона монстру.")
        elif action == 'блок':
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
    """
    Обрабатывает события в четвертой комнате.
    Предлагает игроку двигаться вперед.
    """
    print("Вы находитесь в комнате 4.")
    print("Здесь пусто, но дверь впереди открыта.")
    move = get_input("Введите 'вперед', чтобы пройти дальше: ", ['вперед'])
    if move == 'вперед':
        room_five()

def room_five():
    """
    Обрабатывает события в пятой комнате.
    Игрок может поговорить с мудрецом или двигаться дальше.
    """
    print("Вы находитесь в комнате 5.")
    print("Вы встретили мудреца.")
    action = get_input("Введите 'говорить', чтобы поговорить с мудрецом, "
                       "или 'вперед', чтобы двигаться дальше: ", ['говорить', 'вперед'])
    if action == 'говорить':
        print("Мудрец сказал: 'Будь осторожен в следующей комнате.'")
    room_six()

def room_six():
    """
    Обрабатывает события в шестой комнате.
    Игрок может открыть сундук или двигаться дальше.
    """
    print("Вы находитесь в комнате 6.")
    print("Перед вами большой сундук.")
    action = get_input("Введите 'открыть', чтобы открыть сундук, "
                       "или 'вперед', чтобы пройти дальше: ", ['открыть', 'вперед'])
    if action == 'открыть':
        print("В сундуке лежит золотая корона!")
    room_seven()

def room_seven():
    """
    Обрабатывает события в седьмой комнате.
    Предлагает игроку двигаться вперед.
    """
    print("Вы находитесь в комнате 7.")
    print("Здесь очень темно.")
    move = get_input("Введите 'вперед', чтобы двигаться дальше: ", ['вперед'])
    if move == 'вперед':
        room_eight()

def room_eight():
    """
    Обрабатывает события в восьмой комнате.
    Игрок может сразиться с драконом или убежать.
    """
    print("Вы находитесь в комнате 8.")
    print("Перед вами огромный дракон!")
    action = get_input("Введите 'сразиться', чтобы атаковать дракона, "
                       "или 'бег', чтобы убежать: ", ['сразиться', 'бег'])
    if action == 'сразиться':
        fight_dragon()
    else:
        print("Вы убежали обратно в комнату 7.")
        room_seven()

def fight_dragon():
    """
    Запускает бой с драконом.
    Игрок и дракон обмениваются атаками, пока один не погибнет.
    """
    print("Начинается бой с драконом!")
    player_health = 100
    dragon_health = 200
    while player_health > 0 and dragon_health > 0:
        action = get_input("Введите 'удар', чтобы атаковать дракона, "
                           "или 'блок', чтобы защититься: ", ['удар', 'блок'])
        if action == 'удар':
            damage = random.randint(10, 20)
            dragon_health -= damage
            print(f"Вы нанесли {damage} урона дракону.")
        elif action == 'блок':
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

def game_over():
    """
    Завершает игру и предлагает начать заново.
    """
    print("Конец игры. Хотите сыграть снова?")
    replay = get_input("Введите 'да' для новой игры или 'нет', чтобы выйти: ", ['да', 'нет'])
    if replay == 'да':
        room_one()
    else:
        print("Спасибо за игру!")

def start_game():
    """
    Начинает игру с первой комнаты.
    """
    print("Добро пожаловать в текстовую игру!")
    room_one()

start_game()