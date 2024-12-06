class TennisGameRefactored1:
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
        if self.p1_points == self.p2_points:
            score_output = {
                0: "Love-All",
                1: "Fifteen-All",
                2: "Thirty-All",
                3: "Forty-All",
            }.get(self.p1_points, "Deuce")
        elif self.p1_points >= 4 or self.p2_points >= 4:
            minus_result = self.p1_points - self.p2_points
            if minus_result == 1:
                score_output = f"Advantage {self.player1_name}"
            elif minus_result == -1:
                score_output = f"Advantage {self.player2_name}"
            elif minus_result >= 2:
                score_output = f"Win for {self.player1_name}"
            else:
                score_output = f"Win for {self.player2_name}"
        else:
            score_output += f"{['Love', 'Fifteen', 'Thirty', 'Forty'][self.p1_points]}-"
            score_output += f"{['Love', 'Fifteen', 'Thirty', 'Forty'][self.p2_points]}"
        return score_output


class TennisGameRefactored2:
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
            score_output = f"{['Love', 'Fifteen', 'Thirty', 'Forty'][self.p1_points]}-All"
        if self.p1_points == self.p2_points and self.p1_points >= 4:
            score_output = "Deuce"
        if self.p1_points > 0 and self.p2_points == 0:
            score_output = f"{['Love', 'Fifteen', 'Thirty', 'Forty'][self.p1_points]}-Love"
        if self.p2_points > 0 and self.p1_points == 0:
            score_output = f"Love-{['Love', 'Fifteen', 'Thirty', 'Forty'][self.p2_points]}"
        if self.p1_points > self.p2_points and self.p2_points < 4:
            score_output = (f"{['Love', 'Fifteen', 'Thirty', 'Forty'][self.p1_points]}"
                            f"-{['Love', 'Fifteen', 'Thirty', 'Forty'][self.p2_points]}")
        if self.p2_points > self.p1_points and self.p1_points < 4:
            score_output = (f"{['Love', 'Fifteen', 'Thirty', 'Forty'][self.p1_points]}"
                            f"-{['Love', 'Fifteen', 'Thirty', 'Forty'][self.p2_points]}")
        if self.p1_points >= 4 and self.p2_points >= 0 and (self.p1_points - self.p2_points) >= 2:
            score_output = f"Win for {self.player1_name}"
        if self.p2_points >= 4 and self.p1_points >= 0 and (self.p2_points - self.p1_points) >= 2:
            score_output = f"Win for {self.player2_name}"
        return score_output

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


class TennisGameRefactored3:
    def __init__(self, player1_name, player2_name):
        self.p1_name = player1_name
        self.p2_name = player2_name
        self.p1 = 0
        self.p2 = 0

    def won_point(self, player_name):
        if player_name == self.p1_name:
            self.p1 += 1
        else:
            self.p2 += 1

    def score(self):
        if self.p1 < 4 and self.p2 < 4:
            p = ["Love", "Fifteen", "Thirty", "Forty"]
            s = p[self.p1]
            return f"{s}-All" if self.p1 == self.p2 else f"{s}-{p[self.p2]}"
        elif self.p1 == self.p2:
            return "Deuce"
        else:
            s = self.p1_name if self.p1 > self.p2 else self.p2_name
            return f"Advantage {s}" if abs(self.p1 - self.p2) == 1 else f"Win for {s}"


TennisGame = TennisGameRefactored1
