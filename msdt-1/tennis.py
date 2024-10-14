# -*- coding: utf-8 -*-


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
        if self.p1_points == self.p2_points:
            return {
                0: "Love-All",
                1: "Fifteen-All",
                2: "Thirty-All",
                3: "Forty-All",
            }.get(self.p1_points, "Deuce")

        if self.p1_points >= 4 or self.p2_points >= 4:
            minus_result = self.p1_points - self.p2_points
            if abs(minus_result) == 1:
                return f"Advantage {self.player1_name if minus_result > 0 else self.player2_name}"
            return f"Win for {self.player1_name if minus_result > 0 else self.player2_name}"

        result = "-".join([
            {0: "Love", 1: "Fifteen", 2: "Thirty", 3: "Forty"}[self.p1_points],
            {0: "Love", 1: "Fifteen", 2: "Thirty", 3: "Forty"}[self.p2_points]
        ])
        return result


# NOTE: You must change this to point at the one of the three examples that you're working on!
TennisGame = TennisGameDefactored1
