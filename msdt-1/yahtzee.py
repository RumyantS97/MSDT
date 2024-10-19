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

    def fours(self):
        return self.count_value(self.dice, 4)

    def fives(self):
        return self.count_value(self.dice, 5)

    def sixes(self):
        return self.count_value(self.dice, 6)


    @staticmethod
    def score_pair(d1, d2, d3, d4, d5):
        counts = [0] * 6
        counts[d1 - 1] += 1
        counts[d2 - 1] += 1
        counts[d3 - 1] += 1
        counts[d4 - 1] += 1
        counts[d5 - 1] += 1
        for at in range(6):
            if counts[6 - at - 1] == 2:
                return (6 - at) * 2
        return 0

    @staticmethod
    def two_pair(d1, d2, d3, d4, d5):
        counts = [0] * 6
        counts[d1 - 1] += 1
        counts[d2 - 1] += 1
        counts[d3 - 1] += 1
        counts[d4 - 1] += 1
        counts[d5 - 1] += 1
        n = 0
        score = 0
        for i in range(6):
            if counts[6 - i - 1] == 2:
                n = n + 1
                score += (6 - i)

        if n == 2:
            return score * 2
        else:
            return 0

    @staticmethod
    def four_of_a_kind(_1, _2, d3, d4, d5):
        tallies = [0] * 6
        tallies[_1 - 1] += 1
        tallies[_2 - 1] += 1
        tallies[d3 - 1] += 1
        tallies[d4 - 1] += 1
        tallies[d5 - 1] += 1
        for i in range(6):
            if tallies[i] == 4:
                return (i + 1) * 4
        return 0

    @staticmethod
    def three_of_a_kind(d1, d2, d3, d4, d5):
        t = [0] * 6
        t[d1 - 1] += 1
        t[d2 - 1] += 1
        t[d3 - 1] += 1
        t[d4 - 1] += 1
        t[d5 - 1] += 1
        for i in range(6):
            if t[i] == 3:
                return (i + 1) * 3
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
    def fullHouse(d1, d2, d3, d4, d5):
        _2 = False
        _2_at = 0
        _3 = False
        _3_at = 0

        tallies = [0] * 6
        tallies[d1 - 1] += 1
        tallies[d2 - 1] += 1
        tallies[d3 - 1] += 1
        tallies[d4 - 1] += 1
        tallies[d5 - 1] += 1

        for i in range(6):
            if tallies[i] == 2:
                _2 = True
                _2_at = i + 1

        for i in range(6):
            if tallies[i] == 3:
                _3 = True
                _3_at = i + 1

        if _2 and _3:
            return _2_at * 2 + _3_at * 3
        else:
            return 0
