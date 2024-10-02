from yahtzee import Yahtzee

# These unit tests can be run using the py.test framework
# available from http://pytest.org/

def test_chance_scores_sum_of_all_dice():
    # Тестирование функции подсчета всех очков игральной кости.
    expected = 15
    actual = Yahtzee.calculate_scores_sum_of_all_dice([2,3,4,5,1])
    assert expected == actual
    assert 16 == Yahtzee.calculate_scores_sum_of_all_dice([3,3,4,5,1])


def test_yahtzee_scores_50():
    #  Тестирование функции подсчета очков за Ятци (50 очков).
    expected = 50
    actual = Yahtzee.calculate_yahtzee_score([4,4,4,4,4])
    assert expected == actual
    assert 50 == Yahtzee.calculate_yahtzee_score([6,6,6,6,6])
    assert 0 == Yahtzee.calculate_yahtzee_score([6,6,6,6,3])


def test_calculate_ones_score():
    #  Тестирование функции подсчета очков за однерки.
    assert Yahtzee.calculate_ones_score([1,2,3,4,5]) == 1
    assert 2 == Yahtzee.calculate_ones_score([1,2,1,4,5])
    assert 0 == Yahtzee.calculate_ones_score([6,2,2,4,5])
    assert 4 == Yahtzee.calculate_ones_score([1,2,1,1,1])


def test_calculate_twos_score():
    #  Тестирование функции подсчета очков за двойки.
    assert 4 == Yahtzee.calculate_twos_score([1,2,3,2,6])
    assert 10 == Yahtzee.calculate_twos_score([2,2,2,2,2])


def test_calculate_threes_score():
    #  Тестирование функции подсчета очков за тройки.
    assert 6 == Yahtzee.calculate_threes_score([1,2,3,2,3])
    assert 12 == Yahtzee.calculate_threes_score([2,3,3,3,3])


def test_calculate_fours_score():
    # Тестирование функции подсчета очков за четверки.
    assert 12 == Yahtzee([4,4,4,5,5]).calculate_fours_score()
    assert 8 == Yahtzee([4,4,5,5,5]).calculate_fours_score()
    assert 4 == Yahtzee([4,5,5,5,5]).calculate_fours_score()


def test_calculate_fives_score():
    # Тестирование функции подсчета очков за пятерки.
    assert 10 == Yahtzee([4,4,4,5,5]).calculate_fives_score()
    assert 15 == Yahtzee([4,4,5,5,5]).calculate_fives_score()
    assert 20 == Yahtzee([4,5,5,5,5]).calculate_fives_score()


def test_calculate_sixes_score():
    # Тестирование функции подсчета очков за шестерки.
    assert 0 == Yahtzee([4,4,4,5,5]).calculate_sixes_score()
    assert 6 == Yahtzee([4,4,6,5,5]).calculate_sixes_score()
    assert 18 == Yahtzee([6,5,6,6,5]).calculate_sixes_score()


def test_one_pair_score():
    # Тестирование функции подсчета очков за одну пару.
    assert 6 == Yahtzee.calculate_pair_score([3,4,3,5,6])
    assert 10 == Yahtzee.calculate_pair_score([5,3,3,3,5])
    assert 12 == Yahtzee.calculate_pair_score([5,3,6,6,5])


def test_two_pair_score():
    # Тестирование функции подсчета очков за две пары.
    assert 16 == Yahtzee.calculate_two_pair_score([3,3,5,4,5])
    assert 0 == Yahtzee.calculate_two_pair_score([3,3,5,5,5])


def test_three_of_a_kind_score():
    # Тестирование функции подсчета очков за три одинаковых значения.
    assert 9 == Yahtzee.three_of_a_kind([3,3,3,4,5])
    assert 15 == Yahtzee.three_of_a_kind([5,3,5,4,5])
    assert 0 == Yahtzee.three_of_a_kind([3,3,3,3,5])


def test_four_of_a_knd_score():
    # Тестирование функции подсчета очков за четыре одинаковых значения.
    assert 12 == Yahtzee.calculate_four_of_a_kind_score([3,3,3,3,5])
    assert 20 == Yahtzee.calculate_four_of_a_kind_score([5,5,5,4,5])
    assert 0 == Yahtzee.three_of_a_kind([3,3,3,3,3])


def test_small_straight_score():
    # Тестирование функции подсчета очков за малую последовательность.
    assert 15 == Yahtzee.calculate_small_straight_score([1,2,3,4,5])
    assert 15 == Yahtzee.calculate_small_straight_score([2,3,4,5,1])
    assert 0 == Yahtzee.calculate_small_straight_score([1,2,2,4,5])


def test_large_straight_score():
    # Тестирование функции подсчета очков за большую последовательность.
    assert 20 == Yahtzee.calculate_large_straight_score([6,2,3,4,5])
    assert 20 == Yahtzee.calculate_large_straight_score([2,3,4,5,6])
    assert 0 == Yahtzee.calculate_large_straight_score([1,2,2,4,5])


def test_full_house_score():
    # Тестирование функции подсчета очков за фулл-хаус.
    assert 18 == Yahtzee.calculate_full_house_score([6,2,2,2,6])
    assert 0 == Yahtzee.calculate_full_house_score([2,3,4,5,6])