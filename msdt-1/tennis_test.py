# -*- coding: utf-8 -*-

import pytest
from tennis import TennisGame

from tennis_unittest import test_cases, play_game

class TestTennis:

    @pytest.mark.parametrize('player1_points player2_points score player1_name player2_name'.split(), test_cases)
    def test_get_score(self, player1_points, player2_points, score, player1_name, player2_name):
        game = play_game(player1_points, player2_points, player1_name, player2_name)
        assert score == game.score()
