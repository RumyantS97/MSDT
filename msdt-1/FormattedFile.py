import random
import os
import time

class Character:
    """Класс для создания персонажа и врагов."""

    def __init__(self, name, health, attack_power, defense=0, evasion=0):
        self.name = name.upper()  # Имя персонажа в заглавных буквах
        self.health = health
        self.attack_power = attack_power
        self.defense = defense
        self.evasion = evasion

    def attack(self, other):
        """Атаковать другого персонажа."""
        damage = random.randint(0, self.attack_power) - other.defense
        if damage < 0:
            damage = 0
        other.health -= damage
        print(f"{self.name} атакует {other.name} и наносит {damage} урона.")
        return damage

    def is_alive(self):
        """Проверить, жив ли персонаж."""
        return self.health > 0

    def apply_evasion(self):
        """Проверка на уклонение от атаки."""
        if random.random() < self.evasion:
            print(f"{self.name} увернулся от атаки!")
            return True
        return False


class Item:
    """Класс для предметов в инвентаре."""

    def __init__(self, name, effect, item_type):
        self.name = name.upper()  # Имя предмета в заглавных буквах
        self.effect = effect
        self.item_type = item_type

    def use(self, character):
        """Использовать предмет на персонажа."""
        if self.item_type == "health":
            # Если это обычное зелье здоровья, восстанавливает 30 здоровья
            if self.name == "ЗЕЛЬЕ СУПЕР ИСЦЕЛЕНИЯ":
                character.health += 40  # В два раза больше
            else:
                character.health += 30
            print(f"{character.name} восстанавливает здоровье! Текущее здоровье: {character.health}")
        elif self.item_type == "strength":
            # Если это обычное зелье силы, увеличивает на 5
            if self.name == "ЗЕЛЬЕ СУПЕР СИЛЫ":
                character.attack_power += 10  # В два раза больше
            else:
                character.attack_power += 5
            print(f"{character.name} получает силу атаки! Сила атаки: {character.attack_power}")
        elif self.item_type == "evasion":
            character.evasion += 0.1
            print(f"{character.name} теперь может уклоняться с шансом {character.evasion:.0%}!")


class Inventory:
    """Класс для инвентаря игрока."""

    def __init__(self):
        self.items = []

    def add_item(self, item):
        """Добавить предмет в инвентарь."""
        self.items.append(item)
        print(f"Вы получили предмет: {item.name}")

    def show_inventory(self):
        """Показать инвентарь."""
        if not self.items:
            print("Ваш инвентарь пуст.")
            return
        print("Ваш инвентарь:")
        for item in self.items:
            print(f"- {item.name}: {item.effect}")


class Enemy(Character):
    """Классы для различных типов врагов."""

    def __init__(self, name, health, attack_power, enemy_type, defense=0, evasion=0):
        super().__init__(name, health, attack_power, defense, evasion)
        self.enemy_type = enemy_type

    def display_info(self):
        """Вывод информации о враге."""
        print(f"Тип врага: {self.enemy_type}, Здоровье: {self.health}, Сила атаки: {self.attack_power}")


class Goblin(Enemy):
    """Гоблин с большим урона и слабым здоровьем."""

    def __init__(self):
        super().__init__("ГОБЛИН", random.randint(30, 40), random.randint(20, 25), "Гоблин")


class Orc(Enemy):
    """Орк с высоким здоровьем и средней силой атаки."""

    def __init__(self):
        super().__init__("ОРК", random.randint(50, 60), random.randint(10, 20), "Орк")


class Knight(Enemy):
    """Рыцарь с балансом здоровья и силы атаки."""

    def __init__(self):
        super().__init__("РЫЦАРЬ", random.randint(60, 70), random.randint(12, 18), "Рыцарь")


class Boss(Enemy):
    """Босс с огромным здоровьем и атакой."""

    def __init__(self):
        super().__init__("БОСС", 150, 35, "БОСС")


class Shadow(Enemy):
    """Тень, с теми же параметрами, что и у игрока."""

    def __init__(self, player):
        super().__init__(player.name, player.health, player.attack_power, "ТЕНЬ", player.defense, player.evasion)


class Game:
    """Основной класс игры."""

    def __init__(self):
        self.player = None
        self.enemy = None
        self.inventory = Inventory()
        self.enemy_count = 0

    def create_character(self):
        """Создать персонажа игрока."""
        name = input("Введите имя вашего персонажа: ").upper()  # Имя игрока в заглавных
        health = random.randint(80, 150)  # Увеличиваем здоровье игрока
        attack_power = random.randint(10, 20)
        self.player = Character(name, health, attack_power)
        print(f"Персонаж {self.player.name} создан с {self.player.health} здоровья и {self.player.attack_power} силы атаки.")

    def create_enemy(self):
        """Создать обычного врага."""
        enemy_type = random.choice([Goblin(), Orc(), Knight(), Shadow(self.player)])  # Добавляем шанс на Тень
        self.enemy = enemy_type
        self.enemy.display_info()

    def create_boss(self):
        """Создать босса."""
        self.enemy = Boss()
        self.enemy.display_info()

    def clear_screen(self):
        """Очистить экран."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def player_turn(self):
        """Ход игрока."""
        if self.player.is_alive() and self.enemy.is_alive():
            action = input("Вы хотите атаковать (a), использовать предмет (i) или пропустить ход (s)? ").lower()
            if action == 'a':
                if not self.enemy.apply_evasion():
                    self.player.attack(self.enemy)
                else:
                    print(f"{self.enemy.name} увернулся от атаки!")
            elif action == 'i':
                self.inventory.show_inventory()
                choice = input("Выберите предмет для использования (по имени): ").upper()  # Ввод имени предмета в заглавных
                for item in self.inventory.items:
                    if item.name == choice:
                        item.use(self.player)
                        break
                else:
                    print("Такого предмета нет в инвентаре.")
            elif action == 's':
                print(f"{self.player.name} пропустил ход.")
            else:
                print("Неверный ввод! Ход пропущен.")

    def enemy_turn(self):
        """Ход врага."""
        if self.enemy.is_alive() and not self.player.apply_evasion():
            self.enemy.attack(self.player)
        elif self.player.apply_evasion():
            print(f"{self.player.name} увернулся от атаки!")

    def check_winner(self):
        """Проверить победителя."""
        if not self.player.is_alive():
            print(f"{self.player.name} погиб!")
            return True
        elif not self.enemy.is_alive():
            print(f"{self.enemy.name} повержен!")
            self.enemy_count += 1
            return True
        return False

    def level_up(self):
        """Прокачка игрока."""
        self.player.attack_power += random.randint(5, 10)
        self.player.health += random.randint(10, 20)
        print(f"{self.player.name} прокачался! Теперь сила атаки: {self.player.attack_power}, здоровье: {self.player.health}.")

    def play(self):
        """Основной игровой процесс."""
        self.create_character()

        while self.player.is_alive():
            self.create_enemy()

            while self.enemy.is_alive() and self.player.is_alive():
                self.clear_screen()  # Очистить экран
                self.player_turn()
                if self.check_winner():
                    break
                self.enemy_turn()
                if self.check_winner():
                    break

            # После победы над боссом, появляется тень
            if self.enemy_count == 3:
                self.create_shadow()  # Создаем тень с параметрами игрока
                while not self.check_winner():
                    self.clear_screen()  # Очистить экран
                    self.player_turn()
                    if self.check_winner():
                        break
                    self.enemy_turn()
                    if self.check_winner():
                        break

            # Прокачка
            self.level_up()
            self.enemy_count = 0  # Сброс счетчика врагов

            # Добавление предметов в инвентарь
            if random.random() < 0.5:  # 50% шанс на предмет
                potion = Item("Зелье здоровья", "Восстанавливает 20 здоровья", "health")
                self.inventory.add_item(potion)

            if random.random() < 0.3:  # 30% шанс на зелье силы
                potion = Item("Зелье силы", "Увеличивает силу атаки на 5", "strength")
                self.inventory.add_item(potion)

            # Добавление супер зелья исцеления и супер зелья силы
            if random.random() < 0.2:  # 20% шанс на супер зелье исцеления
                potion = Item("Зелье супер исцеления", "Восстанавливает 40 здоровья", "health")
                self.inventory.add_item(potion)

            if random.random() < 0.2:  # 20% шанс на супер зелье силы
                potion = Item("Зелье супер силы", "Увеличивает силу атаки на 10", "strength")
                self.inventory.add_item(potion)

            print("Хочешь продолжить играть? (y/n)")
            if input().lower() != 'y':
                break

        print("Игра окончена. Спасибо за игру!")


def main():
    """Главная функция для запуска игры."""
    game = Game()
    game.play()


if __name__ == "__main__":
    main()