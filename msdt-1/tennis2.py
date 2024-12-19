class TennisGame2:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.p1_points = 0
        self.p2_points = 0

    def won_point(self, player_name):
        if player_name == "player1":
            self.p1_score()
        else:
            self.p2_score()

    def score(self):
        result = ""
        if self.p1_points == self.p2_points and self.p1_points < 3:
            if self.p1_points == 0:
                result = "Love"
            if self.p1_points == 1:
                result = "Fifteen"
            if self.p1_points == 2:
                result = "Thirty"
            result += "-All"
        if self.p1_points == self.p2_points and self.p1_points > 2:
            result = "Deuce"

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
            result = p1_res + "-" + p2_res
        if self.p2_points > 0 and self.p1_points == 0:
            if self.p2_points == 1:
                p2_res = "Fifteen"
            if self.p2_points == 2:
                p2_res = "Thirty"
            if self.p2_points == 3:
                p2_res = "Forty"

            p1_res = "Love"
            result = p1_res + "-" + p2_res

        if self.p1_points > self.p2_points and self.p1_points < 4:
            if self.p1_points == 2:
                p1_res = "Thirty"
            if self.p1_points == 3:
                p1_res = "Forty"
            if self.p2_points == 1:
                p2_res = "Fifteen"
            if self.p2_points == 2:
                p2_res = "Thirty"
            result = p1_res + "-" + p2_res
        if self.p2_points > self.p1_points and self.p2_points < 4:
            if self.p2_points == 2:
                p2_res = "Thirty"
            if self.p2_points == 3:
                p2_res = "Forty"
            if self.p1_points == 1:
                p1_res = "Fifteen"
            if self.p1_points == 2:
                p1_res = "Thirty"
            result = p1_res + "-" + p2_res

        if self.p1_points > self.p2_points and self.p2_points >= 3:
            result = "Advantage player1"

        if self.p2_points > self.p1_points and self.p1_points >= 3:
            result = "Advantage player2"

        if (
            self.p1_points >= 4
            and self.p2_points >= 0
            and (self.p1_points - self.p2_points) >= 2
        ):
            result = "Win for player1"
        if (
            self.p2_points >= 4
            and self.p1_points >= 0
            and (self.p2_points - self.p1_points) >= 2
        ):
            result = "Win for player2"
        return result

    def set_p1_score(self, number):
        for i in range(number):
            self.p1_score()

    def set_p2_score(self, number):
        for i in range(number):
            self.p2_score()

    def p1_score(self):
        self.p1_points += 1

    def p2_score(self):
        self.p2_points += 1