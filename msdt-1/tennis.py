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
        temp_score=0
        if (self.player1_points==self.player2_points):
            result = {
                0 : "Love-All",
                1 : "Fifteen-All",
                2 : "Thirty-All",
                3 : "Forty-All",
            }.get(self.player1_points, "Deuce")
        elif (self.player1_points>=4 or self.player2_points>=4):
            minusResult = self.player1_points-self.player2_points
            if (minusResult==1):
                result ="Advantage " + self.player1_name
            elif (minusResult ==-1):
                result ="Advantage " + self.player2_name
            elif (minusResult>=2):
                result = "Win for " + self.player1_name
            else:
                result ="Win for " + self.player2_name
        else:
            for i in range(1,3):
                if (i==1):
                    temp_score = self.player1_points
                else:
                    result+="-"
                    temp_score = self.player2_points
                result += {
                    0 : "Love",
                    1 : "Fifteen",
                    2 : "Thirty",
                    3 : "Forty",
                }[temp_score]
        return result


class TennisGameDefactored2:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_points = 0
        self.player2_points = 0
        
    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.P1Score()
        else:
            self.P2Score()
    
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
            if (self.p2points==2):
                player2_result = "Thirty"
            if (self.p2points==3):
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
    
    def SetP1Score(self, number):
        for i in range(number):
            self.P1Score()
    
    def SetP2Score(self, number):
        for i in range(number):
            self.P2Score()
    
    def P1Score(self):
        self.player1_points +=1
    
    
    def P2Score(self):
        self.player2_points +=1
        
class TennisGameDefactored3:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_points = 0
        self.player2_points = 0
        
    def won_point(self, winner_name):
        if winner_name == self.player1_name:
            self.player1_points += 1
        else:
            self.player2_points += 1
    
    def score(self):
        if (self.player1_points < 4 and self.player2_points < 4):
            places = ["Love", "Fifteen", "Thirty", "Forty"]
            result = places[self.player1_points]
            return result + "-All" if (self.player1_points == self.player2_points) else result + "-" + places[self.player2_points]
        else:
            if (self.player1_points == self.player2_points):
                return "Deuce"
            result = self.player1_name if self.player1_points > self.player2_points else self.player2_name
            return "Advantage " + result if ((self.player1_points-self.player2_points)*(self.player1_points-self.player2_points) == 1) else "Win for " + result

# NOTE: You must change this to point at the one of the three examples that you're working on!
TennisGame = TennisGameDefactored1
