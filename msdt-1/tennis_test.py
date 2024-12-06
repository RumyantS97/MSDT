import pytest
from tennis import TennisGame

from tennis_unittest import test_cases, play_game


class TestTennis:

    @pytest.mark.parametrize(
        'player1_points player2_points score player1_mame player2_mame'.split(),
        test_cases
    )
    def test_get_score(
            self,
            player1_points,
            player2_points,
            score,
            player1_mame,
            player2_mame):
        game = play_game(
            player1_points,
            player2_points,
            player1_mame,
            player2_mame)
        assert score == game.score()
