# -*- coding: utf-8 -*-

class TennisGameDefactored1:

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
            minus_result = self.player1_points-self.player2_points
            if minus_result == 1:
                result = "Advantage " + self.player1_name
            elif minus_result == -1:
                result = "Advantage " + self.player2_name
            elif minus_result >= 2:
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
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2Name = player2_name
        self.player1_points = 0
        self.player2_points = 0
        
    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.set_player1_score()
        else:
            self.set_player2_score()
    
    def score(self):
        result = ""
        if (self.player1_points == self.player2_points and self.player1_points < 4):
            if (self.player1_points==0):
                result = "Love"
            if (self.player1_points==1):
                result = "Fifteen"
            if (self.player1_points==2):
                result = "Thirty"
            if (self.player1_points==3):
                result = "Forty"
            result += "-All"
        if (self.player1_points==self.player2_points and self.player1_points>3):
            result = "Deuce"
        
        player1_result = ""
        player2_result = ""
        if (self.player1_points > 0 and self.player2_points==0):
            if (self.player1_points==1):
                player1_result = "Fifteen"
            if (self.player1_points==2):
                player1_result = "Thirty"
            if (self.player1_points==3):
                player1_result = "Forty"
            
            player2_result = "Love"
            result = player1_result + "-" + player2_result
        if (self.player2_points > 0 and self.player1_points==0):
            if (self.player2_points==1):
                player2_result = "Fifteen"
            if (self.player2_points==2):
                player2_result = "Thirty"
            if (self.player2_points==3):
                player2_result = "Forty"
            
            player1_result = "Love"
            result = player1_result + "-" + player2_result
        
        
        if (self.player1_points>self.player2_points and self.player1_points < 4):
            if (self.player1_points==2):
                player1_result="Thirty"
            if (self.player1_points==3):
                player1_result="Forty"
            if (self.player2_points==1):
                player2_result="Fifteen"
            if (self.player2_points==2):
                player2_result="Thirty"
            result = player1_result + "-" + player2_result
        if (self.player2_points>self.player1_points and self.player2_points < 4):
            if (self.player2_points==2):
                player2_result="Thirty"
            if (self.player2_points==3):
                player2_result="Forty"
            if (self.player1_points==1):
                player1_result="Fifteen"
            if (self.player1_points==2):
                player1_result="Thirty"
            result = player1_result + "-" + player2_result
        
        if (self.player1_points > self.player2_points and self.player2_points >= 3):
            result = "Advantage " + self.player1_name
        
        if (self.player2_points > self.player1_points and self.player1_points >= 3):
            result = "Advantage " + self.player2_name
        
        if (self.player1_points>=4 and self.player2_points>=0 and (self.player1_points-self.player2_points)>=2):
            result = "Win for " + self.player1_name
        if (self.player2_points>=4 and self.player1_points>=0 and (self.player2_points-self.player1_points)>=2):
            result = "Win for " + self.player2_name
        return result
    
    def set_player1_score(self, number):
        for i in range(number):
            self.set_player1_score()
    
    def set_player2_score(self, number):
        for i in range(number):
            self.set_player2_score()
    
    def P1Score(self):
        self.player1_points +=1
    
    
    def P2Score(self):
        self.player2_points +=1
        
class TennisGameDefactored3:
    def __init__(self, player1Name, player2Name):
        self.p1N = player1Name
        self.p2N = player2Name
        self.p1 = 0
        self.p2 = 0
        
    def won_point(self, n):
        if n == self.p1N:
            self.p1 += 1
        else:
            self.p2 += 1
    
    def score(self):
        if (self.p1 < 4 and self.p2 < 4):
            p = ["Love", "Fifteen", "Thirty", "Forty"]
            s = p[self.p1]
            return s + "-All" if (self.p1 == self.p2) else s + "-" + p[self.p2]
        else:
            if (self.p1 == self.p2):
                return "Deuce"
            s = self.p1N if self.p1 > self.p2 else self.p2N
            return "Advantage " + s if ((self.p1-self.p2)*(self.p1-self.p2) == 1) else "Win for " + s

# NOTE: You must change this to point at the one of the three examples that you're working on!
TennisGame = TennisGameDefactored1
