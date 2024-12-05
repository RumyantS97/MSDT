class TennisGameDefactored1:

    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.p1_points = 0
        self.p2_points = 0

    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.p1_points += 1
        else:
            self.p2_points += 1

    def score(self):
        score_output = ""
        current_score = 0
        if self.p1_points == self.p2_points:
            score_output = {
                0: "Love-All",
                1: "Fifteen-All",
                2: "Thirty-All",
                3: "Forty-All",
            }.get(self.p1_points, "Deuce")
        elif self.p1_points >= 4 or self.p2_points >= 4:
            minus_result = self.p1_points-self.p2_points
            if minus_result == 1:
                score_output = "Advantage " + self.player1_name
            elif minus_result == -1:
                score_output = "Advantage " + self.player2_name
            elif minus_result >= 2:
                score_output = "Win for " + self.player1_name
            else:
                score_output = "Win for " + self.player2_name
        else:
            for i in range(1, 3):
                if i == 1:
                    current_score = self.p1_points
                else:
                    score_output += "-"
                    current_score = self.p2_points
                score_output += {
                    0: "Love",
                    1: "Fifteen",
                    2: "Thirty",
                    3: "Forty",
                }[current_score]
        return score_output


class TennisGameDefactored2:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.p1_points = 0
        self.p2_points = 0

    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.p1_score()
        else:
            self.p2_score()

    def score(self):
        score_output = ""
        if self.p1_points == self.p2_points and self.p1_points < 4:
            if self.p1_points == 0:
                score_output = "Love"
            if self.p1_points == 1:
                score_output = "Fifteen"
            if self.p1_points == 2:
                score_output = "Thirty"
            if self.p1_points == 3:
                score_output = "Forty"
            score_output += "-All"
        if self.p1_points == self.p2_points and self.p1_points > 3:
            score_output = "Deuce"

        p1_res = ""
        p2_res = ""
        if self.p1_points > 0 and self.p2_points == 0:
            if self.p1_points == 1:
                p1_res = "Fifteen"
            if self.p1_points == 2:
                p1_res = "Thirty"
            if self.p1_points == 3:
                p1_res = "Forty"

            p2_res = "Love"
            score_output = p1_res + "-" + p2_res
        if self.p2_points > 0 and self.p1_points == 0:
            if self.p2_points == 1:
                p2_res = "Fifteen"
            if self.p2_points == 2:
                p2_res = "Thirty"
            if self.p2_points == 3:
                p2_res = "Forty"

            p1_res = "Love"
            score_output = p1_res + "-" + p2_res

        if self.p1_points > self.p2_points and self.p1_points < 4:
            if self.p1_points == 2:
                p1_res = "Thirty"
            if self.p1_points == 3:
                p1_res = "Forty"
            if self.p2_points == 1:
                p2_res = "Fifteen"
            if self.p2_points == 2:
                p2_res = "Thirty"
            score_output = p1_res + "-" + p2_res

        if self.p2_points > self.p1_points and self.p2_points < 4:
            if self.p2_points == 2:
                p2_res = "Thirty"
            if self.p2_points == 3:
                p2_res = "Forty"
            if self.p1_points == 1:
                p1_res = "Fifteen"
            if self.p1_points == 2:
                p1_res = "Thirty"
            score_output = p1_res + "-" + p2_res

        if self.p1_points > self.p2_points and self.p2_points >= 3:
            score_output = "Advantage " + self.player1_name
        if self.p2_points > self.p1_points and self.p1_points >= 3:
            score_output = "Advantage " + self.player2_name

        if self.p1_points >= 4 and self.p2_points >= 0 and (self.p1_points - self.p2_points) >= 2:
            score_output = "Win for " + self.player1_name
        if self.p2_points >= 4 and self.p1_points >= 0 and (self.p2_points - self.p1_points) >= 2:
            score_output = "Win for " + self.player2_name

        return score_output

    def SetP1Score(self, number):
        for i in range(number):
            self.p1_score()

    def SetP2Score(self, number):
        for i in range(number):
            self.p2_score()

    def p1_score(self):
        self.p1_points += 1

    def p2_score(self):
        self.p2_points += 1


class TennisGameDefactored3:
    def __init__(self, player1_name, player2_name):
        self.p1_name = player1_name
        self.p2_name = player2_name
        self.p1 = 0
        self.p2 = 0
        
    def won_point(self, n):
        if n == self.p1_name:
            self.p1 += 1
        else:
            self.p2 += 1
    
    def score(self):
        if self.p1 < 4 and self.p2 < 4:
            p = ["Love", "Fifteen", "Thirty", "Forty"]
            s = p[self.p1]
            return s + "-All" if (self.p1 == self.p2) else s + "-" + p[self.p2]
        else:
            if self.p1 == self.p2:
                return "Deuce"
            s = self.p1_name if self.p1 > self.p2 else self.p2_name
            return "Advantage " + s if ((self.p1-self.p2)*(self.p1-self.p2) == 1) else "Win for " + s


TennisGame = TennisGameDefactored1
