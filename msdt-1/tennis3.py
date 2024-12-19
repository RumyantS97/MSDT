class TennisGame3:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_score = 0
        self.player2_score = 0

    def won_point(self, player_name):
        if player_name == "player1":
            self.player1_score += 1
        else:
            self.player2_score += 1

    def score(self):
        if (self.player1_score < 4 and self.player2_score < 4) and (self.player1_score + self.player2_score < 6):
            p = ["Love", "Fifteen", "Thirty", "Forty"]
            s = p[self.player1_score]
            return s + "-All" if (self.player1_score == self.player2_score) else s + "-" + p[self.player2_score]
        else:
            if self.player1_score == self.player2_score:
                return "Deuce"
            s = self.player1_name if self.player1_score > self.player2_score else self.player2_name
            return (
                "Advantage " + s
                if ((self.player1_score - self.player2_score) * (self.player1_score - self.player2_score) == 1)
                else "Win for " + s
            )