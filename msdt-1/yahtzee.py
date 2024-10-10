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
    def get_counts(dice):
        counts = [0] * 6
        for die in dice:
            counts[die - 1] += 1
        return counts

    @staticmethod
    def small_straight(*dice):
        required = {1, 2, 3, 4, 5}
        return 15 if required.issubset(dice) else 0

    @staticmethod
    def large_straight(*dice):
        required = {2, 3, 4, 5, 6}
        return 20 if required.issubset(dice) else 0

    @staticmethod
    def full_house(*dice):
        counts = Yahtzee.get_counts(dice)
        has_two = 2 in counts
        has_three = 3 in counts
        return sum(dice) if has_two and has_three else 0