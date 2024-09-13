import random
from typing import Callable

from data_types import WordInputOperation
from game_settings import GRID_SIZE, LETTERS_PER_HAND
from letter_points_config import LetterPointsConfig
from tile_types import DEFAULT_CELL, STARTING_CELL, read_tile_types
from word_existence_checker import WordExistenceChecker
from word_points_counter import WordPointsCounter


class Board:
    def __init__(self, log: Callable[[str], None]):
        self.letter_points_config = LetterPointsConfig()
        self.word_existence_checker = WordExistenceChecker()
        self.words: list[str] = []
        self.log = log
        self.tile_types = read_tile_types()
        self.word_points_counter = WordPointsCounter(
            self.letter_points_config, self.tile_types
        )
        self.grid = [[""] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.chips_bag = self.letter_points_config.get_letters_kit()
        self.chips_at_hand: list[str] = [
            self.take_chip() for _ in range(LETTERS_PER_HAND)
        ]

    def take_chip(self) -> str:
        return self.chips_bag.pop(-1)

    def next_chips(self) -> None:
        if len(self.chips_bag) < LETTERS_PER_HAND:
            self.chips_at_hand = [""] * LETTERS_PER_HAND
        else:
            self.chips_at_hand = [self.take_chip() for _ in range(LETTERS_PER_HAND)]

    def release_unused_chips(self, unused_chips: list[str]) -> None:
        self.chips_bag.extend(unused_chips)
        random.shuffle(self.chips_bag)

    def is_word_input_correct(
        self,
        word_letters: list[str],
        word_input: WordInputOperation,
        is_first_word: bool,
    ) -> bool:
        intersect = False
        for i in range(word_input.word_length):
            if word_input.is_horizontal:
                cell_x = word_input.start_cell_x + i
                cell_y = word_input.start_cell_y
            else:
                cell_x = word_input.start_cell_x
                cell_y = word_input.start_cell_y + i

            if is_first_word:
                is_starting_cell = (
                    self.tile_types.get((cell_x, cell_y), DEFAULT_CELL) == STARTING_CELL
                )
                if is_starting_cell:
                    intersect = True
            else:
                if self.grid[cell_x][cell_y] != "":
                    intersect = True

            letter = word_letters[i]
            if letter == "":
                self.log("Empty Space")
                return False

        if not intersect:
            self.log("Слово не пересекается с предыдущими.")
            return False

        result_word = "".join(word_letters)
        if result_word in self.words:
            self.log("Word already been!!!")
            return False

        self.words.append(result_word)
        return self.word_existence_checker.is_valid_word(result_word)

    def input_word(
        self,
        word_letters: list[str],
        word_input: WordInputOperation,
        used_chips_indexes: list[int],
    ):
        for i in range(word_input.word_length):
            if word_input.is_horizontal:
                cell_x = word_input.start_cell_x + i
                cell_y = word_input.start_cell_y
            else:
                cell_x = word_input.start_cell_x
                cell_y = word_input.start_cell_y + i
            self.grid[cell_x][cell_y] = word_letters[i]
        for index in used_chips_indexes:
            self.chips_at_hand[index] = ""

    def word_points(self, info: WordInputOperation) -> int:
        word = self.get_operation_word(info)
        return self.word_points_counter.get_points_for_word(word, info)

    def get_operation_word(self, word_operation: WordInputOperation) -> str:
        letters: list[str] = []
        for i in range(word_operation.word_length):
            if word_operation.is_horizontal:
                cell_x = word_operation.start_cell_x + i
                cell_y = word_operation.start_cell_y
            else:
                cell_x = word_operation.start_cell_x
                cell_y = word_operation.start_cell_y + i
            letters += self.grid[cell_x][cell_y]
        return "".join(letters)

    def close(self) -> None:
        self.letter_points_config.close()
