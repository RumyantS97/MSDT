import random
import os
import time
class Character:
 """Класс для создания персонажа и врагов."""
 def __init__(self,name,health,attack_power,defense=0,evasion=0):
  self.name=name.upper()  #имя персонажа в заглавных буквах
  self.health=health
  self.attack_power=attack_power
  self.defense=defense
  self.evasion=evasion
 def attack(self,other):
  """Атаковать другого персонажа."""
  damage=random.randint(0,self.attack_power) - other.defense
  if damage<0:
   damage=0
  other.health -= damage
  print(f"{self.name} атакует {other.name} и наносит {damage} урона.")
  return damage
 def isalive(self):
  """Проверить,жив ли персонаж."""
  return self.health>0
 def applyevasion(self):
  """Проверка на уклонение от атаки."""
  if random.random()<self.evasion:
   print(f"{self.name} увернулся от атаки!")
   return True
  return False
class Item:
 """Класс для предметов в инвентаре."""
 def __init__(self,name,effect,item_type):
  self.name=name.upper()  #имя предмета в заглавных буквах
  self.effect=effect
  self.item_type=item_type
 def use(self,character):
  """Использовать предмет на персонажа."""
  if self.item_type == "health":
   #если это обычное зелье здоровья,восстанавливает 30 здоровья
   if self.name == "ЗЕЛЬЕ СУПЕР ИСЦЕЛЕНИЯ":
    character.health+=40  #в два раза больше
   else:
    character.health+=30
   print(f"{character.name} восстанавливает здоровье! Текущее здоровье: {character.health}")
  elif self.item_type == "strength":
   #если это обычное зелье силы,увеличивает на 5
   if self.name == "ЗЕЛЬЕ СУПЕР СИЛЫ":
    character.attack_power+=10  #в два раза больше
   else:
    character.attack_power+=5
   print(f"{character.name} получает силу атаки! Сила атаки: {character.attack_power}")
  elif self.item_type == "evasion":
   character.evasion+=0.1
   print(f"{character.name} теперь может уклоняться с шансом {character.evasion:.0%}!")
class Inventory:
 """Класс для инвентаря игрока."""
 def __init__(self):
  self.items=[]
 def add_item(self,item):
  """Добавить предмет в инвентарь."""
  self.items.append(item)
  print(f"Вы получили предмет: {item.name}")
 def showinventory(self):
  """Показать инвентарь."""
  if not self.items:
   print("Ваш инвентарь пуст.")
   return
  print("Ваш инвентарь:")
  for item in self.items:
   print(f"- {item.name}: {item.effect}")
class Enemy(Character):
 """Классы для различных типов врагов."""
 def __init__(self,name,health,attack_power,enemy_type,defense=0,evasion=0):
  super().__init__(name,health,attack_power,defense,evasion)
  self.enemy_type=enemy_type
 def displayinfo(self):
  """Вывод информации о враге."""
  print(f"Тип врага: {self.enemy_type},Здоровье: {self.health},Сила атаки: {self.attack_power}")
class Goblin(Enemy):
 """Гоблин с большим урона и слабым здоровьем."""
 def __init__(self):
  super().__init__("ГОБЛИН",random.randint(30,40),random.randint(20,25),"Гоблин")
class Orc(Enemy):
 """Орк с высоким здоровьем и средней силой атаки."""
 def __init__(self):
  super().__init__("ОРК",random.randint(50,60),random.randint(10,20),"Орк")
class Knight(Enemy):
 """Рыцарь с балансом здоровья и силы атаки."""
 def __init__(self):
  super().__init__("РЫЦАРЬ",random.randint(60,70),random.randint(12,18),"Рыцарь")
class Boss(Enemy):
 """Босс с огромным здоровьем и атакой."""
 def __init__(self):
  super().__init__("БОСС",150,35,"БОСС")
class Shadow(Enemy):
 """Тень,с теми же параметрами,что и у игрока."""
 def __init__(self,player):
  super().__init__(player.name,player.health,player.attack_power,"ТЕНЬ",player.defense,player.evasion)
class Game:
 """Основной класс игры."""
 def __init__(self):
  self.player=None
  self.enemy=None
  self.inventory=Inventory()
  self.enemy_count=0
 def createcharacter(self):
  """Создать персонажа игрока."""
  name=input("Введите имя вашего персонажа: ").upper()  #имя игрока в заглавных
  health=random.randint(80,150)  #увеличиваем здоровье игрока
  attack_power=random.randint(10,20)
  self.player=Character(name,health,attack_power)
  print(f"Персонаж {self.player.name} создан с {self.player.health} здоровья и {self.player.attack_power} силы атаки.")
 def createenemy(self):
  """Создать обычного врага."""
  enemy_type=random.choice([Goblin(),Orc(),Knight(),Shadow(self.player)])  #добавляем шанс на Тень
  self.enemy=enemy_type
  self.enemy.displayinfo()
 def createboss(self):
  """Создать босса."""
  self.enemy=Boss()
  self.enemy.displayinfo()
 def clearscreen(self):
  """Очистить экран."""
  os.system('cls' if os.name == 'nt' else 'clear')
 def playerturn(self):
  """Ход игрока."""
  if self.player.isalive() and self.enemy.isalive():
   action=input("Вы хотите атаковать (a),использовать предмет (i) или пропустить ход (s)? ").lower()
   if action == 'a':
    if not self.enemy.applyevasion():
     self.player.attack(self.enemy)
    else:
     print(f"{self.enemy.name} увернулся от атаки!")
   elif action == 'i':
    self.inventory.showinventory()
    choice=input("Выберите предмет для использования (по имени): ").upper()  #ввод имени предмета в заглавных
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
 def enemyturn(self):
  """Ход врага."""
  if self.enemy.isalive() and not self.player.applyevasion():
   self.enemy.attack(self.player)
  elif self.player.applyevasion():
   print(f"{self.player.name} увернулся от атаки!")
 def checkwinner(self):
  """Проверить победителя."""
  if not self.player.isalive():
   print(f"{self.player.name} погиб!")
   return True
  elif not self.enemy.isalive():
   print(f"{self.enemy.name} повержен!")
   self.enemy_count+=1
   return True
  return False
 def levelup(self):
  """Прокачка игрока."""
  self.player.attack_power+=random.randint(5,10)
  self.player.health+=random.randint(10,20)
  print(f"{self.player.name} прокачался! Теперь сила атаки: {self.player.attack_power},здоровье: {self.player.health}.")
 def play(self):
  """Основной игровой процесс."""
  self.createcharacter()
  while self.player.isalive():
   self.createenemy()
   while self.enemy.isalive() and self.player.isalive():
    self.clearscreen()  #очистить экран
    self.playerturn()
    if self.checkwinner():
     break
    self.enemyturn()
    if self.checkwinner():
     break
   #после победы над боссом,появляется тень
   if self.enemy_count == 3:
    self.createboss()  #создаем тень с параметрами игрока
    while not self.checkwinner():
     self.clearscreen()  #очистить экран
     self.playerturn()
     if self.checkwinner():
      break
     self.enemyturn()
     if self.checkwinner():
      break
   #прокачка
   self.levelup()
   self.enemy_count=0  #сброс счетчика врагов
   #добавление предметов в инвентарь
   if random.random()<0.5:  #50% шанс на предмет
    potion=Item("Зелье здоровья","Восстанавливает 20 здоровья","health")
    self.inventory.add_item(potion)
   if random.random()<0.3:  #30% шанс на зелье силы
    potion=Item("Зелье силы","Увеличивает силу атаки на 5","strength")
    self.inventory.add_item(potion)
   #добавление супер зелья исцеления и супер зелья силы
   if random.random()<0.2:  #20% шанс на супер зелье исцеления
    potion=Item("Зелье супер исцеления","Восстанавливает 40 здоровья","health")
    self.inventory.add_item(potion)
   if random.random()<0.2:  #20% шанс на супер зелье силы
    potion=Item("Зелье супер силы","Увеличивает силу атаки на 10","strength")
    self.inventory.add_item(potion)
   print("Хочешь продолжить играть? (y/n)")
   if input().lower() != 'y':
    break
  print("Игра окончена. Спасибо за игру!")
def main():
 """Главная функция для запуска игры."""
 game=Game()
 game.play()
if __name__ == "__main__":
 main()
