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
            score_names = ["Love", "Fifteen", "Thirty", "Forty"]
            player1_score_name = score_names[self.player1_score]
            return player1_score_name + "-All" if (self.player1_score == self.player2_score) else player1_score_name + "-" + score_names[self.player2_score]
        else:
            if self.player1_score == self.player2_score:
                return "Deuce"
            leading_player = self.player1_name if self.player1_score > self.player2_score else self.player2_name
            return (
                "Advantage " + leading_player
                if ((self.player1_score - self.player2_score) * (self.player1_score - self.player2_score) == 1)
                else "Win for " + leading_player
            )