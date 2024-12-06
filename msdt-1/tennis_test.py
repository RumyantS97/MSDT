import pytest
from tennis import TennisGame

from tennis_unittest import test_cases, play_game


class TestTennis:

    @pytest.mark.parametrize('p1_points p2_points score p1_mame p2_mame'.split(), test_cases)
    def test_get_score(self, p1_points, p2_points, score, p1_mame, p2_mame):
        game = play_game(p1_points, p2_points, p1_mame, p2_mame)
        assert score == game.score()
