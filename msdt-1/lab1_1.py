class TennisGameDefactored1:
    """
    A class representing a tennis game, tracking players'
    scores and providing the current score.
    """

    def __init__(self, player1_name: str, player2_name: str) -> None:
        """
        Initializes the game with player names and sets initial scores to zero.

        Args:
            player1_name (str): Name of the first player.
            player2_name (str): Name of the second player.
        """
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_points = 0
        self.player2_points = 0

    def won_point(self, player_name: str) -> None:
        """
        Increases the score of the player who won the point.

        Args:
            player_name (str): Name of the player who won the point.
        """
        if player_name == self.player1_name:
            self.player1_points += 1
        else:
            self.player2_points += 1

    def score(self) -> str:
        """
        Calculates and returns the current score of the game in tennis scoring format.

        Returns:
            str: The current score in terms of "Love", "Fifteen", "Thirty", "Forty",
                 "Deuce", "Advantage", or "Win".
        """
        result = ""
        temp_score = 0

        if self.player1_points == self.player2_points:
            result = {
                0: "Love-All",
                1: "Fifteen-All",
                2: "Thirty-All",
                3: "Forty-All",
            }.get(self.player1_points, "Deuce")
        elif self.player1_points >= 4 or self.player2_points >= 4:
            point_difference = self.player1_points - self.player2_points
            if point_difference == 1:
                result = "Advantage " + self.player1_name
            elif point_difference == -1:
                result = "Advantage " + self.player2_name
            elif point_difference >= 2:
                result = "Win for " + self.player1_name
            else:
                result = "Win for " + self.player2_name
        else:
            for i in range(1, 3):
                if i == 1:
                    temp_score = self.player1_points
                else:
                    result += "-"
                    temp_score = self.player2_points
                result += {
                    0: "Love",
                    1: "Fifteen",
                    2: "Thirty",
                    3: "Forty",
                }[temp_score]

        return result


class TennisGameDefactored2:
    """
    A class to track points in a tennis game with additional methods for handling
    score setting and calculation.
    """

    def __init__(self, player1_name: str, player2_name: str) -> None:
        """
        Initializes the game with player names and sets initial scores to zero.

        Args:
            player1_name (str): Name of the first player.
            player2_name (str): Name of the second player.
        """
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_points = 0
        self.player2_points = 0

    def won_point(self, player_name: str) -> None:
        """
        Increases the score of the player who won the point.

        Args:
            player_name (str): Name of the player who won the point.
        """
        if player_name == self.player1_name:
            self.increase_player1_score()
        else:
            self.increase_player2_score()

    def score(self) -> str:
        """
        Returns the current score of the game using tennis score terminology.

        Returns:
            str: The current score of the game, including special cases for "Deuce",
                 "Advantage", and "Win".
        """
        result = ""
        if self.player1_points == self.player2_points and \
            self.player1_points < 4:
            result = (
                ["Love", "Fifteen", "Thirty", "Forty"][self.player1_points] + "-All"
            )
        elif self.player1_points == self.player2_points and \
            self.player1_points >= 3:
            result = "Deuce"
        else:
            player1_score_text = (
                ["Love", "Fifteen", "Thirty", "Forty"][self.player1_points]
                if self.player1_points < 4 else ""
            )
            player2_score_text = (
                ["Love", "Fifteen", "Thirty", "Forty"][self.player2_points]
                if self.player2_points < 4 else ""
            )
            if self.player1_points > self.player2_points and \
                self.player1_points >= 4:
                result = "Advantage " + self.player1_name
            elif self.player2_points > self.player1_points and \
                self.player2_points >= 4:
                result = "Advantage " + self.player2_name
            elif self.player1_points >= 4 and \
                self.player1_points - self.player2_points >= 2:
                result = "Win for " + self.player1_name
            elif self.player2_points >= 4 and \
                self.player2_points - self.player1_points >= 2:
                result = "Win for " + self.player2_name
            else:
                result = player1_score_text + "-" + player2_score_text

        return result

    def set_player1_score(self, number: int) -> None:
        """
        Sets the score for player 1.

        Args:
            number (int): The number of points to add to player 1's score.
        """
        for _ in range(number):
            self.increase_player1_score()

    def set_player2_score(self, number: int) -> None:
        """
        Sets the score for player 2.

        Args:
            number (int): The number of points to add to player 2's score.
        """
        for _ in range(number):
            self.increase_player2_score()

    def increase_player1_score(self) -> None:
        """Increases player 1's score by one point."""
        self.player1_points += 1

    def increase_player2_score(self) -> None:
        """Increases player 2's score by one point."""
        self.player2_points += 1


class TennisGameDefactored3:
    """
    A class representing a tennis game with an optimized scoring system.
    """

    def __init__(self, player1_name: str, player2_name: str) -> None:
        """
        Initializes the game with player names and sets initial scores to zero.

        Args:
            player1_name (str): Name of the first player.
            player2_name (str): Name of the second player.
        """
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_points = 0
        self.player2_points = 0

    def won_point(self, player_name: str) -> None:
        """
        Increases the score of the player who won the point.

        Args:
            player_name (str): Name of the player who won the point.
        """
        if player_name == self.player1_name:
            self.player1_points += 1
        else:
            self.player2_points += 1

    def score(self) -> str:
        """
        Returns the current score of the game using tennis terminology.

        Returns:
            str: The current score, including special cases for "Deuce",
              "Advantage", and "Win".
        """
        points = ["Love", "Fifteen", "Thirty", "Forty"]

        if self.player1_points < 4 and self.player2_points < 4 and \
            self.player1_points + self.player2_points < 6:
            if self.player1_points == self.player2_points:
                return f"{points[self.player1_points]}-All"
            else:
                return f"{points[self.player1_points]}-{points[self.player2_points]}"

        if self.player1_points == self.player2_points:
            return "Deuce"

        if abs(self.player1_points - self.player2_points) == 1:
            return f"Advantage {self.player1_name if self.player1_points > \
                                self.player2_points else self.player2_name}"

        return f"Win for {self.player1_name if self.player1_points > \
                          self.player2_points else self.player2_name}"