class Yahtzee:
    @staticmethod
    def calculate_scores_sum_of_all_dice(dice):
        #  Суммирует все значения игральной кости.
        # Параметр dice обозначает список целых чисел, представляющих значения игральной кости.
        return sum(dice)


    @staticmethod
    def calculate_yahtzee_score(dice):
        # Вычисляет очки в игре Ятзи на основе значений кубиков.
        # Параметр dice обозначает список значений кубиков.
        counts = [0] * (len(dice) + 1)
        for die in dice:
            counts[die - 1] += 1
        for i in range(len(counts)):
            if counts[i] == 5:
                return 50
        return 0
    

    @staticmethod
    def calculate_ones_score(dice):
        # Подсчитывает очки за единицы в списке значений кигральной кости.
        # Параметр dice обозначает список целых чисел, представляющих значения игральной кости.
        return sum( 1 for d in dice if d == 1)
    

    @staticmethod
    def calculate_twos_score(dice):
        # Подсчитывает очки за двойки в списке значений игральной кости.
        # Параметр dice обозначает список целых чисел, представляющих значения игральной кости.
        return sum(2 for d in dice if d == 2)
    
    
    @staticmethod
    def calculate_threes_score(dice):
        # Подсчитывает очки за тройки в списке значений игральной кости.
        # Параметр dice обозначает список целых чисел, представляющих значения игральной кости.
        return sum(3 for d in dice if d == 3)
    

    def __init__(self, args):
        # Параметр dice обозначает список целых чисел, представляющих значения игральной кости.
        self.dice = [0] * 5  
        if len(args) != 5:
           raise ValueError("Должно быть ровно 5 элементов.")
        self.dice = args
    
    
    def calculate_fours_score(self):
        # Подсчитывает очки за четверки в списке значений игральной кости.
        sum = 0
        for value in range(5):
            if (self.dice[value] == 4): 
                sum += 4
        return sum
    

    def calculate_fives_score(self):
        # Подсчитывает очки за пятерки в списке значений игральной кости.
        sum = 0
        i = 0
        for i in range(len(self.dice)): 
            if (self.dice[i] == 5):
                sum = sum + 5
        return sum
    

    def calculate_sixes_score(self):
        # Подсчитывает очки за шестерки в списке значений игральной кости.
        sum = 0
        for at in range(len(self.dice)): 
            if (self.dice[at] == 6):
                sum = sum + 6
        return sum
    

    @staticmethod
    def calculate_pair_score(dice):
        # Подсчитывает очки за одну пару в списке значений игральной кости.
        # Параметр dice обозначает список целых чисел, представляющих значения игральной кости.
        if len(dice) != 5:
            raise ValueError("Должно быть ровно 5 элементов.")
    
        counts = [0] * 6
        for value in dice:
            counts[value - 1] += 1

        for i in range(6):
            if (counts[6 - i - 1] == 2):
                return (6 - i) * 2
            
        return 0
    

    @staticmethod
    def calculate_two_pair_score(dice):
        # Подсчитывает очки за две пары в списке значений игральной кости.
        # Параметр dice обозначает список целых чисел, представляющих значения игральной кости.
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
    def calculate_four_of_a_kind_score(dice):
        #Подсчитывает очки за четыре одинаковых значения в списке значений игральной кости.
        # Параметр dice обозначает список целых чисел, представляющих значения игральной кости.
        tallies = [0] * 6

        for value in dice:
            tallies[value - 1] += 1
       
        for i in range(6):
            if (tallies[i] == 4):
                return (i + 1) * 4
        return 0
    

    @staticmethod
    def calculate_three_of_a_kind_score(dice):
        # Подсчитывает очки за три одинаковых значения в списке значений игральной кости.
        # Параметр dice обозначает список целых чисел, представляющих значения игральной кости.
        tallies = [0] * 6

        for value in dice:
            tallies[value - 1] += 1

        for i in range(6):
            if (tallies[i] == 3):
                return (i + 1) * 3
        return 0
    

    @staticmethod
    def calculate_small_straight_score(dice):
        # Проверяет наличие малой стрит-комбинации и подсчитывает за нее очки.
        # Параметр dice обозначает список целых чисел, представляющих значения игральной кости.
        tallies = [0] * 6

        for value in dice:
            tallies[value - 1] += 1

        if all(tallies[i] == 1 for i in range(5)):
            return 15
        
        return 0
    

    @staticmethod
    def calculate_large_straight_score(dice):
        # Проверяет наличие большой стрит-комбинации и подсчитывает за нее очки.
        # Параметр dice обозначает список целых чисел, представляющих значения игральной кости.
        tallies = [0] * 6
        
        for value in dice:
            tallies[value - 1] += 1

        if all(tallies[i] == 1 for i in range(1, 6)):
            return 20
        
        return 0
    

    @staticmethod
    def calculate_full_house_score(dice):
        # Подсчитывает очки за фулл-хаус в списке значений кубиков.
        # Параметр dice обозначает список целых чисел, представляющих значения игральной кости.
        tallies = [] * 6
        key_2 = False
        i = 0
        sum_2 = 0
        key_3 = False
        sum_3  = 0

        for value in dice:
            tallies[value - 1] += 1

        for i in range(6):
            if (tallies[i] == 2): 
                key_2 = True
                sum_2 = i + 1
            

        for i in range(6):
            if (tallies[i] == 3): 
                key_3 = True
                sum_3 = i + 1
            

        if (key_2 and key_3):
            return sum_2 * 2 + sum_3 * 3
        else:
            return 0