class Item:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.level = 1
        self.experience = 0
        self.inventory = []

    def add_item(self, item):
        self.inventory.append(item)


def save_game(player):
    """Save the player's game state to a file."""
    with open(f"{player.name}_save.txt", "w") as f:
        f.write(f"{player.name}\n")
        f.write(f"{player.hp}\n")
        f.write(f"{player.level}\n")
        f.write(f"{player.experience}\n")
        for item in player.inventory:
            f.write(f"{item.name}\n")


def load_game():
    """Load the player's game state from a file."""
    name = input("Enter your character's name to load: ")
    try:
        with open(f"{name}_save.txt", "r") as f:
            player_name = f.readline().strip()
            hp = int(f.readline().strip())
            level = int(f.readline().strip())
            experience = int(f.readline().strip())
            player = Player(player_name)
            player.hp = hp
            player.level = level
            player.experience = experience
            items = f.readlines()
            for item_name in items:
                player.add_item(Item(item_name.strip(), 20))
            print("Game loaded successfully!")
            return player
    except FileNotFoundError:
        print("Save file not found.")
        return None


def explore(player):
    """Explore the dungeon and encounter monsters or items."""
    # Exploration logic goes here
    pass


def main():
    """Main function to start the game."""
    player_name = input("Enter your character's name: ")
    player = Player(player_name)
    while True:
        action = input("Do you want to (1) Save, (2) Load, (3) Explore, or (4) Quit? ")
        if action == "1":
            save_game(player)
        elif action == "2":
            player = load_game()
            if player:
                print(f"Welcome back, {player.name}!")
        elif action == "3":
            explore(player)
        elif action == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
