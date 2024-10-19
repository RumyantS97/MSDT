class Yahtzee:

    @staticmethod
    def chance(*dice):
        return sum(dice)

    @staticmethod
    def yahtzee(dice):
        return 50 if dice.count(dice[0]) == 5 else 0

    @staticmethod
    def ones(d1, d2, d3, d4, d5):
        total_sum = 0
        if d1 == 1:
            total_sum += 1
        if d2 == 1:
            total_sum += 1
        if d3 == 1:
            total_sum += 1
        if d4 == 1:
            total_sum += 1
        if d5 == 1:
            total_sum += 1

        return total_sum

    @staticmethod
    def twos(d1, d2, d3, d4, d5):
        total_sum = 0
        if d1 == 2:
            total_sum += 2
        if d2 == 2:
            total_sum += 2
        if d3 == 2:
            total_sum += 2
        if d4 == 2:
            total_sum += 2
        if d5 == 2:
            total_sum += 2
        return total_sum

    @staticmethod
    def threes(d1, d2, d3, d4, d5):
        s = 0
        if d1 == 3:
            s += 3
        if d2 == 3:
            s += 3
        if d3 == 3:
            s += 3
        if d4 == 3:
            s += 3
        if d5 == 3:
            s += 3
        return s

    def __init__(self, *dice):
        self.dice = list(dice)

    def fours(self):
        total_sum = 0
        for at in range(5):
            if self.dice[at] == 4:
                total_sum += 4
        return total_sum

    def fives(self):
        s = 0
        for i in range(len(self.dice)):
            if self.dice[i] == 5:
                s = s + 5
        return s

    def sixes(self):
        total_sum = 0
        for at in range(len(self.dice)):
            if self.dice[at] == 6:
                total_sum = total_sum + 6
        return total_sum

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
