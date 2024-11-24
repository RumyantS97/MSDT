class TennisGame1:
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
        if self.player1_points == self.player2_points:
            return self._get_equal_score()
        elif self.player1_points >= 4 or self.player2_points >= 4:
            return self._get_advantage_or_win_score()
        else:
            return self._get_normal_score()
    
    def _get_equal_score(self):
        return {
            0: "Love-All",
            1: "Fifteen-All",
            2: "Thirty-All",
            3: "Forty-All",
        }.get(self.player1_points, "Deuce")
    
    def _get_advantage_or_win_score(self):
        minus_result = self.player1_points - self.player2_points
        if minus_result == 1:
            return f"Advantage {self.player1_name}"
        elif minus_result == -1:
            return f"Advantage {self.player2_name}"
        elif minus_result >= 2:
            return f"Win for {self.player1_name}"
        else:
            return f"Win for {self.player2_name}"
    
    def _get_normal_score(self):
        score_names = ["Love", "Fifteen", "Thirty", "Forty"]
        player1_score = score_names[self.player1_points]
        player2_score = score_names[self.player2_points]
        return f"{player1_score}-{player2_score}"

class TennisGame2:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_points = 0
        self.player2_points = 0
        
    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.p1_score()
        else:
            self.p2_score()
    
    def score(self):
        result = ""
        if self.player1_points == self.player2_points and self.player1_points < 4:
            if self.player1_points == 0:
                result = "Love"
            if self.player1_points == 1:
                result = "Fifteen"
            if self.player1_points == 2:
                result = "Thirty"
            if self.player1_points == 3:
                result = "Forty"
            result += "-All"
        if self.player1_points == self.player2_points and self.player1_points > 3:
            result = "Deuce"
        
        p1_res = ""
        p2_res = ""
        if self.player1_points > 0 and self.player2_points == 0:
            if self.player1_points == 1:
                p1_res = "Fifteen"
            if self.player1_points == 2:
                p1_res = "Thirty"
            if self.player1_points == 3:
                p1_res = "Forty"
            
            p2_res = "Love"
            result = f"{p1_res}-{p2_res}"
        if self.player2_points > 0 and self.player1_points == 0:
            if self.player2_points == 1:
                p2_res = "Fifteen"
            if self.player2_points == 2:
                p2_res = "Thirty"
            if self.player2_points == 3:
                p2_res = "Forty"
            
            p1_res = "Love"
            result = f"{p1_res}-{p2_res}"
    
      if self.player1_points > 0 and self.player2_points == 0:
            return f"{p1_res}-Love"
        if self.player2_points > 0 and self.player1_points == 0:
            return f"Love-{p2_res}"
        
        if self.player1_points > self.player2_points and self.player1_points < 4:
            return f"{p1_res}-{p2_res}"
        if self.player2_points > self.player1_points and self.player2_points < 4:
            return f"{p1_res}-{p2_res}"
        
        if self.player1_points > self.player2_points and self.player2_points >= 3:
            return f"Advantage {self.player1_name}"
        if self.player2_points > self.player1_points and self.player1_points >= 3:
            return f"Advantage {self.player2_name}"
        
        if self.player1_points >= 4 and self.player2_points >= 0 and (self.player1_points - self.player2_points) >= 2:
            return f"Win for {self.player1_name}"
        if self.player2_points >= 4 and self.player1_points >= 0 and (self.player2_points - self.player1_points) >= 2:
            return f"Win for {self.player2_name}"
    
    def _get_score_name(self, points):
        score_names = ["Love", "Fifteen", "Thirty", "Forty"]
        return score_names[points] if points < 4 else "Forty"
    
    def set_p1_score(self, number):
        for i in range(number):
            self.p1_score()
    
    def set_p2_score(self, number):
        for i in range(number):
            self.p2_score()
    
    def p1_score(self):
        self.player1_points += 1
    
    def p2_score(self):
        self.player2_points += 1
        
lass TennisGame3:
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
        if self.player1_points < 4 and self.player2_points < 4:
            return self._get_normal_score()
        else:
            return self._get_advantage_or_win_score()
    
    def _get_normal_score(self):
        score_names = ["Love", "Fifteen", "Thirty", "Forty"]
        player1_score = score_names[self.player1_points]
        return f"{player1_score}-All" if self.player1_points == self.player2_points else f"{player1_score}-{score_names[self.player2_points]}"
    
    def _get_advantage_or_win_score(self):
        if self.player1_points == self.player2_points:
            return "Deuce"
        leading_player = self.player1_name if self.player1_points > self.player2_points else self.player2_name
        return f"Advantage {leading_player}" if abs(self.player1_points - self.player2_points) == 1 else f"Win for {leading_player}"

TennisGame = TennisGame3
