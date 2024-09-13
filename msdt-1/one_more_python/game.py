import random
import time

class Player:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.score = 0
        self.items = []
        self.health = 100
        self.energy = 100
        self.experience = 0
        self.strength = 5
        self.defense = 5

    def attack(self, other_player):
        if self.energy > 0:
            damage = random.randint(1, self.strength)
            other_player.health -= damage
            self.energy -= 10
            print(f'{self.name} attacked {other_player.name} for {damage} damage. {other_player.name} has {other_player.health} health left.')
            if other_player.health <= 0:
                print(f'{other_player.name} is defeated!')
                self.gain_experience(10)
        else:
            print(f'{self.name} is too tired to attack!')

    def rest(self):
        print(f'{self.name} is resting...')
        self.energy += 20
        if self.energy > 100:
            self.energy = 100
        time.sleep(2)
        print(f'{self.name} now has {self.energy} energy.')

    def gain_experience(self, amount):
        self.experience += amount
        print(f'{self.name} gained {amount} experience. Total experience: {self.experience}')
        if self.experience >= 50:
            self.level_up()

    def level_up(self):
        self.strength += 1
        self.defense += 1
        self.experience = 0
        print(f'{self.name} leveled up! Strength is now {self.strength} and defense is now {self.defense}.')

    def collect_item(self, item):
        self.items.append(item)
        print(f'{self.name} collected {item}.')

    def show_status(self):
        print(f'Player {self.name}: Health: {self.health}, Energy: {self.energy}, Score: {self.score}, Experience: {self.experience}, Strength: {self.strength}, Defense: {self.defense}, Items: {self.items}')

class Game:
    def __init__(self):
        self.players = []
        self.items = ['Sword', 'Shield', 'Potion', 'Bow', 'Helmet', 'Armor', 'Boots']
        self.enemies = ['Goblin', 'Orc', 'Dragon', 'Troll']
        self.game_over = False

    def add_player(self, name, age):
        player = Player(name, age)
        self.players.append(player)

    def start_game(self):
        print('Game has started!')
        self.game_loop()

    def game_loop(self):
        while not self.game_over:
            for player in self.players:
                print(f"\nIt's {player.name}'s turn.")
                player.show_status()
                action = input('Choose action: 1-Attack, 2-Rest, 3-Collect item, 4-End game\n')
                if action == '1':
                    if len(self.players) > 1:
                        opponent = self.choose_opponent(player)
                        player.attack(opponent)
                    else:
                        print('No other players to attack.')
                elif action == '2':
                    player.rest()
                elif action == '3':
                    item = random.choice(self.items)
                    player.collect_item(item)
                elif action == '4':
                    self.end_game()
                else:
                    print('Invalid action!')

                if self.check_game_over():
                    break

    def choose_opponent(self, current_player):
        opponents = [p for p in self.players if p != current_player]
        if opponents:
            return random.choice(opponents)
        return None

    def check_game_over(self):
        alive_players = [p for p in self.players if p.health > 0]
        if len(alive_players) <= 1:
            print('Game over! We have a winner.')
            self.game_over = True
            return True
        return False

    def end_game(self):
        print('Ending the game.')
        self.game_over = True

    def spawn_enemy(self):
        enemy = random.choice(self.enemies)
        print(f'An enemy {enemy} appeared!')
        return enemy

def another_function_that_is_completely_unrelated():
    print("This function has no purpose but to add more lines of code.")
    for i in range(20):
        print(f'This is a random loop, iteration {i}. It does nothing.')

def yet_another_useless_function():
    result = 0
    for i in range(10):
        for j in range(10):
            result += i * j
    print(f'The meaningless result is {result}.')

def complex_function_that_could_be_simplified():
    x = 10
    y = 20
    if x == 10:
        if y == 20:
            for i in range(5):
                print(f'Nested loops and conditions! Iteration {i}.')
                if i % 2 == 0:
                    if x + y > 30:
                        print('Deep nesting and unnecessary complexity.')
    else:
        print('This path is never taken.')

if __name__ == '__main__':
    game = Game()
    game.add_player('Alice', 20)
    game.add_player('Bob', 22)
    game.start_game()
    another_function_that_is_completely_unrelated()
    yet_another_useless_function()
    complex_function_that_could_be_simplified()
