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
            minus_result = self.player1_points - self.player2_points
            if minus_result == 1:
                result = f"Advantage {self.player1_name}"
            elif minus_result == -1:
                result = f"Advantage {self.player2_name}"
            elif minus_result >= 2:
                result = f"Win for {self.player1_name}"
            else:
                result = f"Win for {self.player2_name}"
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
            result = p1_res + "-" + p2_res
        if self.player2_points > 0 and self.player1_points == 0:
            if self.player2_points == 1:
                p2_res = "Fifteen"
            if self.player2_points == 2:
                p2_res = "Thirty"
            if self.player2_points == 3:
                p2_res = "Forty"
            
            p1_res = "Love"
            result = p1_res + "-" + p2_res
        
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
        
        if self.player1_points > self.player2_points and self.player1_points < 4:
            if self.player1_points == 2:
                p1_res = "Thirty"
            if self.player1_points == 3:
                p1_res = "Forty"
            if self.player2_points == 1:
                p2_res = "Fifteen"
            if self.player2_points == 2:
                p2_res = "Thirty"
            result = f"{p1_res}-{p2_res}"
        if self.player2_points > self.player1_points and self.player2_points < 4:
            if self.player2_points == 2:
                p2_res = "Thirty"
            if self.player2_points == 3:
                p2_res = "Forty"
            if self.player1_points == 1:
                p1_res = "Fifteen"
            if self.player1_points == 2:
                p1_res = "Thirty"
            result = f"{p1_res}-{p2_res}"
        
        if self.player1_points > self.player2_points and self.player2_points >= 3:
            result = f"Advantage {self.player1_name}"
        
        if self.player2_points > self.player1_points and self.player1_points >= 3:
            result = f"Advantage {self.player2_name}"
        
        if self.player1_points >= 4 and self.player2_points >= 0 and (self.player1_points - self.player2_points) >= 2:
            result = f"Win for {self.player1_name}"
        if self.player2_points >= 4 and self.player1_points >= 0 and (self.player2_points - self.player1_points) >= 2:
            result = f"Win for {self.player2_name}"
        return result
    
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
        
class TennisGame3:
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
            score_names = ["Love", "Fifteen", "Thirty", "Forty"]
            player1_score = score_names[self.player1_points]
            return f"{player1_score}-All" if self.player1_points == self.player2_points else f"{player1_score}-{score_names[self.player2_points]}"
        else:
            if self.player1_points == self.player2_points:
                return "Deuce"
            leading_player = self.player1_name if self.player1_points > self.player2_points else self.player2_name
            return f"Advantage {leading_player}" if abs(self.player1_points - self.player2_points) == 1 else f"Win for {leading_player}"

TennisGame = TennisGame3
