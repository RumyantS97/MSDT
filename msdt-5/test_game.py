import pytest as pytest
from main import *
from RandomWords import easy_wordlist, medium_wordlist, hard_wordlist
from unittest.mock import Mock
import string

global DIFFICULTY_LEVEL


def test_word_easy():
    word=get_word("easy")
    word.lower()
    status=0
    for a in easy_wordlist:
        if a.upper()==word:
            status=1
    assert status==1

def test_word_medium():
    word=get_word("medium")
    word.lower()
    status=0
    for a in medium_wordlist:
        if a.upper()==word:
            status=1
    assert status==1


def test_hangman_0():
    test=hangman(0)
    picture= """
                           --------
                           |      |
                           |      O
                           |     \\|/
                           |      ||
                           |     // \\
                           -
                        """
    assert test==picture


def test_hangman_8():
    test=hangman(8)
    picture=   """
                   --------
                   |      |
                   |      
                   |    
                   |      
                   |     
                   -
                """
    assert test==picture

def test_hangman_3():
    test=hangman(3)
    picture=  """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / 
                   -
                """
    assert test==picture

@pytest.mark.parametrize("difficulty", [
    ("easy"),
    ("medium"),
    ("hard"),
])
def test_all_difficulties(difficulty):
    if difficulty=="easy":
        word_list=easy_wordlist
    if difficulty == "medium":
        word_list = medium_wordlist
    if difficulty == "hard":
        word_list = hard_wordlist
    word = get_word(difficulty)
    word.lower()
    for a in word_list:
        if a.upper()==word:
            status=1
    assert status==1

@pytest.mark.parametrize("difficulty, expected", [
    ("easy", 8),
    ("medium", 6),
    ("hard", 4),
])
def test_choose_difficulty(difficulty, expected):
    difficulty_number=choose_difficulty(difficulty)
    assert difficulty_number==expected



