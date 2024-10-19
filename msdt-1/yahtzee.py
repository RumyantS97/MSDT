from collections import Counter

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
    def fours(self):
        return self.count_value(self.dice, 4)

    @staticmethod
    def fives(self):
        return self.count_value(self.dice, 5)

    @staticmethod
    def sixes(self):
        return self.count_value(self.dice, 6)

    @staticmethod
    def score_pair(*dice):
        counts = Counter(dice)
        for num in range(6, 0, -1):
            if counts[num] >= 2:
                return num * 2
        return 0

    @staticmethod
    def two_pair(*dice):
        counts = Counter(dice)
        pairs = [num for num, count in counts.items() if count >= 2]
        if len(pairs) >= 2:
            return sum(pairs[:2]) * 2
        return 0

    @staticmethod
    def three_of_a_kind(*dice):
        counts = Counter(dice)
        for num in range(6, 0, -1):
            if counts[num] >= 3:
                return num * 3
        return 0

    @staticmethod
    def four_of_a_kind(*dice):
        counts = Counter(dice)
        for num in range(6, 0, -1):
            if counts[num] >= 4:
                return num * 4
        return 0

    @staticmethod
    def smallStraight(*dice):
        required = {1, 2, 3, 4, 5}
        return 15 if required.issubset(dice) else 0

    @staticmethod
    def largeStraight(*dice):
        required = {2, 3, 4, 5, 6}
        return 20 if required.issubset(dice) else 0

    @staticmethod
    def full_house(*dice):
        counts = Counter(dice)
        has_three = has_two = 0
        for num, count in counts.items():
            if count == 3:
                has_three = num
            elif count == 2:
                has_two = num
        if has_three and has_two:
            return has_three * 3 + has_two * 2
        return 0
