class Yahtzee:
    @staticmethod
    def chance(dice):
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
    def ones(dice):
        return sum( 1 for d in dice if d == 1)
    

    @staticmethod
    def twos(dice):
        return sum(2 for d in dice if d == 2)
    
    
    @staticmethod
    def threes(dice):
        return sum(3 for d in dice if d == 3)
    

    def __init__(self, args):
        self.dice = [0] * 5  
        if len(args) != 5:
           raise ValueError("Должно быть ровно 5 элементов.")
        self.dice = args
    
    
    def fours(self):
        sum = 0
        for at in range(5):
            if (self.dice[at] == 4): 
                sum += 4
        return sum
    

    def fives(self):
        s = 0
        i = 0
        for i in range(len(self.dice)): 
            if (self.dice[i] == 5):
                s = s + 5
        return s
    

    def sixes(self):
        sum = 0
        for at in range(len(self.dice)): 
            if (self.dice[at] == 6):
                sum = sum + 6
        return sum
    

    @staticmethod
    def score_pair(dice):
        if len(dice) != 5:
            raise ValueError("Должно быть ровно 5 элементов.")
    
        counts = [0] * 6
        for value in dice:
            counts[value - 1] += 1

        for at in range(6):
            if (counts[6 - at - 1] == 2):
                return (6 - at) * 2
            
        return 0
    

    @staticmethod
    def two_pair(dice):
        if len(dice) != 5:
            raise ValueError("Должно быть ровно 5 элементов.")
    
        counts = [0] * 6
        for value in dice:
            counts[value - 1] += 1

        n = 0
        score = 0
        for i in range(6):
            if (counts[6 - i - 1] == 2):
                n = n+1
                score += (6 - i)
                    
        if (n == 2):
            return score * 2
        else:
            return 0
    

    @staticmethod
    def four_of_a_kind(dice):
        tallies = [0] * 6

        for value in dice:
            tallies[value - 1] += 1
       
        for i in range(6):
            if (tallies[i] == 4):
                return (i + 1) * 4
        return 0
    

    @staticmethod
    def three_of_a_kind(dice):
        t = [0] * 6

        for value in dice:
            t[value - 1] += 1

        for i in range(6):
            if (t[i] == 3):
                return (i + 1) * 3
        return 0
    

    @staticmethod
    def smallStraight(dice):
        tallies = [0] * 6

        for value in dice:
            tallies[value - 1] += 1

        if all(tallies[i] == 1 for i in range(5)):
            return 15
        
        return 0
    

    @staticmethod
    def largeStraight(dice):
        tallies = [0] * 6
        
        for value in dice:
            tallies[value - 1] += 1

        if all(tallies[i] == 1 for i in range(1, 6)):
            return 20
        
        return 0
    

    @staticmethod
    def fullHouse(dice):
        tallies = [] * 6
        _2 = False
        i = 0
        _2_at = 0
        _3 = False
        _3_at = 0

        for value in dice:
            tallies[value - 1] += 1

        for i in range(6):
            if (tallies[i] == 2): 
                _2 = True
                _2_at = i + 1
            

        for i in range(6):
            if (tallies[i] == 3): 
                _3 = True
                _3_at = i + 1
            

        if (_2 and _3):
            return _2_at * 2 + _3_at * 3
        else:
            return 0