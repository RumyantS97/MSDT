import random

class Character:
    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.attack = attack

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, dmg):
        print(f"{self.name} takes {dmg} damage.")  # Примитивное логирование
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0

    def heal(self, amount):
        print(f"{self.name} heals for {amount} HP.")  # Примитивное логирование
        self.hp += amount
        if self.hp > 100:
            self.hp = 100

class Player(Character):
    def __init__(self, name):
        super().__init__(name, 100, 10)
        self.inventory = []

    def add_item(self, item):
        print(f"{self.name} adds {item} to inventory.")  # Примитивное логирование
        self.inventory.append(item)

    def show_inventory(self):
        print("Inventory:")
        for item in self.inventory:
            print(f"- {item}")

class Monster(Character):
    def __init__(self, name, hp, attack):
        super().__init__(name, hp, attack)

def create_monster():
    names = ["Goblin", "Orc", "Troll"]
    name = random.choice(names)
    hp = random.randint(20, 50)
    attack = random.randint(5, 15)
    return Monster(name, hp, attack)

def battle(player, monster):
    print(f"A wild {monster.name} appears!")  # Примитивное логирование
    while player.is_alive() and monster.is_alive():
        action = input("Do you want to (a)ttack or (r)un? ")
        if action == "a":
            monster.take_damage(player.attack)
            print(f"You attacked {monster.name} for {player.attack} damage!")  # Примитивное логирование
            if monster.is_alive():
                player.take_damage(monster.attack)
                print(f"{monster.name} attacked you for {monster.attack} damage!")  # Примитивное логирование
        elif action == "r":
            print("You ran away!")  # Примитивное логирование
            break
        else:
            print("Invalid action!")

def explore(player):
    print("You are exploring the dungeon...")  # Примитивное логирование
    while player.is_alive():
        encounter = random.choice(["monster", "item", "nothing"])
        if encounter == "monster":
            monster = create_monster()
            battle(player, monster)
        elif encounter == "item":
            item = "Health Potion"
            print(f"You found a {item}!")  # Примитивное логирование
            take_item = input("Do you want to take it? (y/n) ")
            if take_item == "y":
                player.add_item(item)
        else:
            print("You found nothing.")  # Примитивное логирование

def main():
    print("Welcome to the Dungeon Explorer!")  # Примитивное логирование
    player_name = input("Enter your character's name: ")
    player = Player(player_name)
    while player.is_alive():
        action = input("Do you want to (e)xplore or (i)nventory? ")
        if action == "e":
            explore(player)
        elif action == "i":
            player.show_inventory()
        else:
            print("Invalid action!")

    print("Game Over!")  # Примитивное логирование

if __name__ == "__main__":
    main()
