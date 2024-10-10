class Yahtzee:

    @staticmethod
    def chance(*dice):
        return sum(dice)

    @staticmethod
    def yahtzee(dice):
        return 50 if dice.count(dice[0]) == 5 else 0

    @staticmethod
    def count_value(dice, value):
        return dice.count(value) * value

    @staticmethod
    def ones(*dice):
        return Yahtzee.count_value(dice, 1)

    @staticmethod
    def twos(*dice):
        return Yahtzee.count_value(dice, 2)

    @staticmethod
    def threes(*dice):
        return Yahtzee.count_value(dice, 3)

    @staticmethod
    def ones(d1, d2, d3, d4, d5):
        total = 0
        if d1 == 1:
            total += 1
        if d2 == 1:
            total += 1
        if d3 == 1:
            total += 1
        if d4 == 1:
            total += 1
        if d5 == 1:
            total += 1
        return total

    @staticmethod
    def twos(d1, d2, d3, d4, d5):
        total = 0
        if d1 == 2:
            total += 2
        if d2 == 2:
            total += 2
        if d3 == 2:
            total += 2
        if d4 == 2:
            total += 2
        if d5 == 2:
            total += 2
        return total

    @staticmethod
    def threes(d1, d2, d3, d4, d5):
        total = 0
        if d1 == 3:
            total += 3
        if d2 == 3:
            total += 3
        if d3 == 3:
            total += 3
        if d4 == 3:
            total += 3
        if d5 == 3:
            total += 3
        return total
