class TennisGameRefactored1:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_points = 0
        self.player2_points = 0

    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.player1_points += 1
        else:
            self.player2_points += 1

    def score(self):
        score_output = ""
        if self.player1_points == self.player2_points:
            score_output = {
                0: "Love-All",
                1: "Fifteen-All",
                2: "Thirty-All",
                3: "Forty-All",
            }.get(self.player1_points, "Deuce")
        elif self.player1_points >= 4 or self.player2_points >= 4:
            minus_result = self.player1_points - self.player2_points
            if minus_result == 1:
                score_output = f"Advantage {self.player1_name}"
            elif minus_result == -1:
                score_output = f"Advantage {self.player2_name}"
            elif minus_result >= 2:
                score_output = f"Win for {self.player1_name}"
            else:
                score_output = f"Win for {self.player2_name}"
        else:
            score_output += (
                # Эту строку не сократить до <=79 символов (с учетом отступов),
                # иначе, если грубо ставить переносы строки, нарушается pep8.
                f"{['Love', 'Fifteen', 'Thirty', 'Forty'][self.player1_points]}-"
            )
            score_output += (
                # Аналогично
                f"{['Love', 'Fifteen', 'Thirty', 'Forty'][self.player2_points]}"
            )
        return score_output


class TennisGameRefactored2:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_points = 0
        self.player2_points = 0

    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.player1_score()
        else:
            self.player2_score()

    def score(self):
        score_output = ""
        if (
                self.player1_points == self.player2_points
                and self.player1_points < 4
        ):
            score_output = (
                # Из-за нового осмысленного имени для переменной невозможно
                # добиться длины строки <=79 (с учетом отступов).
                # Аналогично для строк ниже..
                f"{['Love', 'Fifteen', 'Thirty', 'Forty'][self.player1_points]}-All"
            )

        if (
                self.player1_points == self.player2_points
                and self.player1_points >= 4
        ):
            score_output = "Deuce"

        if self.player1_points > 0 and self.player2_points == 0:
            score_output = (
                f"{['Love', 'Fifteen', 'Thirty', 'Forty'][self.player1_points]}-Love"
            )

        if self.player2_points > 0 and self.player1_points == 0:
            score_output = (
                f"Love-{['Love', 'Fifteen', 'Thirty', 'Forty'][self.player2_points]}"
            )

        if (
                self.player1_points > self.player2_points
                and self.player2_points < 4
        ):
            score_output = (
                f"{['Love', 'Fifteen', 'Thirty', 'Forty'][self.player1_points]}-"
                f"{['Love', 'Fifteen', 'Thirty', 'Forty'][self.player2_points]}"
            )

        if (
                self.player2_points > self.player1_points
                and self.player1_points < 4
        ):
            score_output = (
                f"{['Love', 'Fifteen', 'Thirty', 'Forty'][self.player1_points]}-"
                f"{['Love', 'Fifteen', 'Thirty', 'Forty'][self.player2_points]}"
            )

        if (
                self.player1_points >= 4
                and self.player2_points >= 0
                and (self.player1_points - self.player2_points) >= 2
        ):
            score_output = f"Win for {self.player1_name}"

        if (
                self.player2_points >= 4
                and self.player1_points >= 0
                and (self.player2_points - self.player1_points) >= 2
        ):
            score_output = f"Win for {self.player2_name}"

        return score_output

    def set_player1_score(self, number):
        for i in range(number):
            self.player1_score()

    def set_player2_score(self, number):
        for i in range(number):
            self.player2_score()

    def player1_score(self):
        self.player1_points += 1

    def player2_score(self):
        self.player2_points += 1


class TennisGameRefactored3:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1 = 0
        self.player2 = 0

    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.player1 += 1
        else:
            self.player2 += 1

    def score(self):
        if self.player1 < 4 and self.player2 < 4:
            score_names = ["Love", "Fifteen", "Thirty", "Forty"]
            current_score = score_names[self.player1]
            return (
                f"{current_score}-All" if self.player1 == self.player2
                else f"{current_score}-{score_names[self.player2]}")
        elif self.player1 == self.player2:
            return "Deuce"
        else:
            current_score = (
                self.player1_name if self.player1 > self.player2
                else self.player2_name
            )
            return (
                f"Advantage {current_score}"
                if abs(self.player1 - self.player2) == 1
                else f"Win for {current_score}"
            )


TennisGame = TennisGameRefactored1
