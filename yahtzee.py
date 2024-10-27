class Yahtzee:

    @staticmethod
    def chance(d1, d2, d3, d4, d5):
        total_sum = d1 + d2 + d3 + d4 + d5
        return total_sum

    @staticmethod
    def yahtzee(dice):
        counts = [0] * (len(dice) + 1)
        for die in dice:
            counts[die - 1] += 1
        for i in range(len(counts)):
            if counts[i] == 5:
                return 50
        return 0

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
        total_sum = 0
        if d1 == 3:
            total_sum += 3
        if d2 == 3:
            total_sum += 3
        if d3 == 3:
            total_sum += 3
        if d4 == 3:
            total_sum += 3
        if d5 == 3:
            total_sum += 3
        return total_sum

    def __init__(self, d1, d2, d3, d4, _5):
        self.dice = [0] * 5
        self.dice[0] = d1
        self.dice[1] = d2
        self.dice[2] = d3
        self.dice[3] = d4
        self.dice[4] = _5

    def fours(self):
        total_sum = 0
        for die in range(5):
            if self.dice[die] == 4:
                total_sum += 4
        return total_sum

    def fives(self):
        total_sum = 0
        for die in self.dice:
            if die == 5:
                total_sum += 5
        return total_sum

    def sixes(self):
        total_sum = 0
        for die in self.dice:
            if die == 6:
                total_sum += 6
        return total_sum

    @staticmethod
    def score_pair(d1, d2, d3, d4, d5):
        counts = [0] * 6
        counts[d1 - 1] += 1
        counts[d2 - 1] += 1
        counts[d3 - 1] += 1
        counts[d4 - 1] += 1
        counts[d5 - 1] += 1
        for i in range(6):
            if counts[6 - i - 1] == 2:
                return (6 - i) * 2
        return 0

    @staticmethod
    def two_pair(d1, d2, d3, d4, d5):
        counts = [0] * 6
        counts[d1 - 1] += 1
        counts[d2 - 1] += 1
        counts[d3 - 1] += 1
        counts[d4 - 1] += 1
        counts[d5 - 1] += 1
        pairs = 0
        score = 0
        for i in range(6):
            if counts[6 - i - 1] == 2:
                pairs += 1
                score += (6 - i) * 2
        if pairs == 2:
            return score
        return 0

    @staticmethod
    def four_of_a_kind(d1, d2, d3, d4, d5):
        counts = [0] * 6
        counts[d1 - 1] += 1
        counts[d2 - 1] += 1
        counts[d3 - 1] += 1
        counts[d4 - 1] += 1
        counts[d5 - 1] += 1
        for i in range(6):
            if counts[i] == 4:
                return (i + 1) * 4
        return 0

    @staticmethod
    def three_of_a_kind(d1, d2, d3, d4, d5):
        counts = [0] * 6
        counts[d1 - 1] += 1
        counts[d2 - 1] += 1
        counts[d3 - 1] += 1
        counts[d4 - 1] += 1
        counts[d5 - 1] += 1
        for i in range(6):
            if counts[i] == 3:
                return (i + 1) * 3
        return 0

    @staticmethod
    def small_straight(d1, d2, d3, d4, d5):
        dice = sorted([d1, d2, d3, d4, d5])
        if dice == [1, 2, 3, 4, 5]:
            return 15
        return 0

    @staticmethod
    def large_straight(d1, d2, d3, d4, d5):
        dice = sorted([d1, d2, d3, d4, d5])
        if dice == [2, 3, 4, 5, 6]:
            return 20
        return 0

    @staticmethod
    def full_house(d1, d2, d3, d4, d5):
        counts = [0] * 6
        counts[d1 - 1] += 1
        counts[d2 - 1] += 1
        counts[d3 - 1] += 1
        counts[d4 - 1] += 1
        counts[d5 - 1] += 1
        has_two = False
        has_three = False
        for count in counts:
            if count == 2:
                has_two = True
            elif count == 3:
                has_three = True
        if has_two and has_three:
            return sum([d1, d2, d3, d4, d5])
        return 0
