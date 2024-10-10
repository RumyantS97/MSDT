class Yahtzee:

    @staticmethod
    def chance(*dice):
        return sum(dice)

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
