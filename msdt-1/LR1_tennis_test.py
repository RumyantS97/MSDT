import pytest

from LR1_tennis import TennisGame

from LR1_unittest import test_cases, play_game


class TestTennis:

    @pytest.mark.parametrize(
        'p1_points p2_points score p1_name p2_name'.split(), test_cases)
    def test_get_score(self, p1_points, p2_points, score, p1_name, p2_name):
        game = play_game(p1_points, p2_points, p1_name, p2_name)
        assert score == game.score()
