import random
import logging

# Настройка логирования
logging.basicConfig(
    filename='game_log.txt',  # Имя файла для сохранения логов
    level=logging.INFO,        # Уровень логирования (INFO и выше)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Формат записей в логе
)

class Character:
    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.attack = attack
        # Логируем создание персонажа
        logging.info(f"Character created: {self.name} (HP: {self.hp}, Attack: {self.attack})")

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, dmg):
        self.hp -= dmg
        # Логируем получение урона
        logging.info(f"{self.name} takes {dmg} damage. Remaining HP: {self.hp}")
        if self.hp < 0:
            self.hp = 0

    def heal(self, amount):
        self.hp += amount
        if self.hp > 100:
            self.hp = 100
        # Логируем исцеление персонажа
        logging.info(f"{self.name} heals for {amount} HP. Current HP: {self.hp}")

class Player(Character):
    def __init__(self, name):
        super().__init__(name, 100, 10)
        self.inventory = []

    def add_item(self, item):
        self.inventory.append(item)
        # Логируем добавление предмета в инвентарь
        logging.info(f"{self.name} adds {item} to inventory.")

    def show_inventory(self):
        # Логируем проверку инвентаря
        logging.info(f"{self.name} checks inventory.")
        return self.inventory

class Monster(Character):
    def __init__(self, name, hp, attack):
        super().__init__(name, hp, attack)

def create_monster():
    names = ["Goblin", "Orc", "Troll"]
    name = random.choice(names)
    hp = random.randint(20, 50)
    attack = random.randint(5, 15)
    # Логируем создание монстра
    logging.info(f"Monster created: {name} (HP: {hp}, Attack: {attack})")
    return Monster(name, hp, attack)

def battle(player, monster):
    # Логируем появление монстра
    logging.info(f"A wild {monster.name} appears!")
    while player.is_alive() and monster.is_alive():
        action = input("Do you want to (a)ttack or (r)un? ")
        if action == "a":
            monster.take_damage(player.attack)
            # Логируем атаку игрока
            logging.info(f"{player.name} attacked {monster.name} for {player.attack} damage!")
            if monster.is_alive():
                player.take_damage(monster.attack)
                # Логируем атаку монстра
                logging.info(f"{monster.name} attacked {player.name} for {monster.attack} damage!")
        elif action == "r":
            # Логируем бегство игрока
            logging.info(f"{player.name} ran away from {monster.name}.")
            break
        else:
            print("Invalid action!")

def explore(player):
    # Логируем исследование подземелья
    logging.info(f"{player.name} is exploring the dungeon...")
    while player.is_alive():
        encounter = random.choice(["monster", "item", "nothing"])
        if encounter == "monster":
            monster = create_monster()
            battle(player, monster)
        elif encounter == "item":
            item = "Health Potion"
            print(f"You found a {item}!")
            take_item = input("Do you want to take it? (y/n) ")
            if take_item == "y":
                player.add_item(item)
        else:
            # Логируем, если ничего не найдено
            logging.info(f"{player.name} found nothing.")

def main():
    # Логируем начало игры
    logging.info("Game started.")
    print("Welcome to the Dungeon Explorer!")
    player_name = input("Enter your character's name: ")
    player = Player(player_name)
    while player.is_alive():
        action = input("Do you want to (e)xplore or (i)nventory? ")
        if action == "e":
            explore(player)
        elif action == "i":
            inventory = player.show_inventory()
            print("Inventory:", inventory)
        else:
            print("Invalid action!")

    # Логируем окончание игры
    logging.info("Game Over!")
    print("Game Over!")

if __name__ == "__main__":
    main()
