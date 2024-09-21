from random import choice
class Card:
    def __init__(self, rang, suit):
        self.rang = rang
        self.suit = suit

    def __str__(self):
        return str(self.rang) + str(self.suit)


class Deck:
    rangs = [*range(2, 11), 'J', 'Q', 'K', 'A']
    suits = ['♥', '♣', '♦', '♠']

    def __init__(self):
        self.cards = [Card(rang, suit) for rang in self.rangs for suit in self.suits]

    def __getitem__(self, item):
        if 0 <= item < len(self.cards):
            return self.cards[item]
        else:
            return None

    def __len__(self):
        return len(self.cards)


class Player:

    def __init__(self):
        self.cards = []
        self.count = 0

    def __getitem__(self, item):
        if 0 <= item < len(self.cards):
            return self.cards[item]
        else:
            return None

    def append(self, card: Card):
        self.cards.append(card)
        if card.rang in ('J', 'Q', 'K'):
            self.count += 10
        elif card.rang == 'A':
            if self.count >= 11:
                self.count += 1
            else:
                self.count += 11
        else:
            self.count += card.rang

def get_info(user: Player, dealer: Player):
    print('=' * 30)
    print('Карты дилера: ', *dealer.cards)
    print('Очки дилера: ' + str(dealer.count))
    print('Ваши карты: ', *user.cards)
    print('Ваши очки: ' + str(user.count))
    print('=' * 30)

def user_check(user: Player):
    if user.count > 21:
        return False
    elif user.count == 21:
        return True
    else:
        return None

def dealer_check(dealer: Player):
    if dealer.count>21:
        return True
    elif dealer.count==21:
        return False
    else:
        return None

def main(points: int):
    bet = input('У вас ' + str(points) + ' очков.\nСколько вы хотите поставить? ')
    while not bet.isdigit() and int(bet) <= points:
        bet = input('Ваша ставка должна быть числом, меньшим общего количества очков: ')
    bet = int(bet)
    deck = Deck()
    user = Player()
    dealer = Player()
    dealer.append(choice(deck))
    user.append(choice(deck))
    user.append(choice(deck))
    get_info(user, dealer)
    if user.count == 21:
        if 10 <= dealer.count <= 11:
            if dealer.count == 11:
                choice1 = input('''У вас блэк-джек, но у дилера на руках туз. 
                Вы можете остаться при своих или продолжить играть.
                О - остаться, П - продолжить ''')
                while not choice1 in ('О', 'П'):
                    choice1 = input('Введите ответ в соответствии с инструкциями ')
                if choice1 == 'О':
                    return points
        else:
            print('Поздравляем! У вас блэк-джек! Ваш очки: ' + str(points * 1.5))
            return points + bet
    if user.count != 21:
        flag = True
        while flag:
            choice1 = input('Будете брать карту? (да/нет) ')
            while not choice1 in ('да', 'нет'):
                choice1 = input('Введите ответ в соответствии с инструкциями ')
            if choice1 == 'да':
                user.append(choice(deck))
                get_info(user, dealer)
                check = user_check(user)
                if check is not None:
                    if check:
                        print('У вас 21')
                        flag = False
                    else:
                        print('У вас > 21! Вы проиграли!')
                        return points - bet
            else:
                flag = False
    print('Дилер берёт карты')
    flag = True
    while flag:
        if dealer.count < 17:
            dealer.append(choice(deck))
        else:
            flag = False
    get_info(user, dealer)
    check = dealer_check(dealer)
    if check is not None:
        if check:
            print('У дилера > 21! Вы выиграли!')
            return points + bet
        else:
            print('У дилера 21')
            if user.count == 21:
                print('Ничья')
                return points
            else:
                print('Вы проиграли!')
                return points - bet
    if user.count > dealer.count:
        print('Вы выиграли!')
        return points + bet
    elif user.count == dealer.count:
        print('Ничья')
        return points
    else:
        print('Вы проиграли!')
        return points - bet


points = input('Введите количество очков: ')
while not points.isdigit():
    points = input('Введите число: ')
points = int(points)
flag = True
while flag:
    points = main(points)
    print('Ваши очки: ' + str(points))
    if points > 0:
        asnwer = input('Хотите сыграть ещё? (да/нет) ')
        while not asnwer in ('да', 'нет'):
            asnwer = input('Введите ответ в соответствии с инструкциями ')
        if asnwer == 'нет':
            flag = False
    else:
        print('У вас закончились очки')
        input()
        flag = False