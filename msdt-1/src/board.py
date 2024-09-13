import random
from typing import Callable, TypeAlias

from PyQt5.QtWidgets import QPushButton

from data_types import WordInputOperation
from game_settings import GRID_SIZE, LETTERS_PER_HAND
from letter_points_config import LetterPointsConfig
from tile_types import DEFAULT_CELL, STARTING_CELL, read_tile_types
from word_existence_checker import WordExistenceChecker
from word_points_counter import WordPointsCounter

ButtonsGrid: TypeAlias = list[list[QPushButton]]
ButtonsForHand: TypeAlias = list[QPushButton]


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

    def update_chips(self, buttons: ButtonsForHand) -> None:
        for chip, button in zip(self.chips_at_hand, buttons):
            button.setText(chip)
            if chip != "":
                button.setToolTip(
                    f"Очков за букву: {self.letter_points_config.get_letter_value(chip)}"
                )
            else:
                button.setToolTip("")

    def update_grid(self, buttons: ButtonsGrid) -> None:
        for i, buttons_row in zip(self.grid, buttons):
            for letter, button in zip(i, buttons_row):
                if letter != "":
                    button.setEnabled(False)
                button.setText(letter)

    def update_boosters(self, buttons: ButtonsGrid) -> None:
        for i, line in enumerate(buttons):
            for j, btn in enumerate(line):
                btn.setProperty("boost", self.tile_types.get((i, j), DEFAULT_CELL))

    def commit_grid(self, buttons: ButtonsGrid, chips: ButtonsForHand) -> None:
        for i, line in enumerate(buttons):
            for j, btn in enumerate(line):
                self.grid[i][j] = btn.text()
        for i, chip in enumerate(chips):
            self.chips_at_hand[i] = chip.text()

    def release_unused_chips(self, buttons: ButtonsForHand, cursor: str | None) -> None:
        for button in buttons:
            if button.text() != "":
                self.chips_bag.append(button.text())
                print(button.text())
        if cursor is not None:
            self.chips_bag.append(cursor)
            print(cursor)
        random.shuffle(self.chips_bag)

    def input_word(
        self, buttons: ButtonsGrid, word_input: WordInputOperation, fist_word: bool
    ) -> bool:
        result_word = ""
        intersect = False
        for i in range(word_input.word_length):
            if word_input.is_horizontal:
                cell_x = word_input.start_cell_x + i
                cell_y = word_input.start_cell_y
            else:
                cell_x = word_input.start_cell_x
                cell_y = word_input.start_cell_y + i

            button = buttons[cell_x][cell_y]
            if not fist_word:
                intersect = True
            if (
                fist_word
                and self.tile_types.get((cell_x, cell_y), DEFAULT_CELL) == STARTING_CELL
            ):
                intersect = True
            let = button.text()
            if let == "":
                self.log("Empty Space")
                return False
            result_word += let
        if result_word in self.words:
            self.log("Word already been!!!")
            return False
        self.words.append(result_word)
        if not intersect:
            self.log("Слово не пересекается с предыдущими.")
            return False
        return self.word_existence_checker.is_valid_word(result_word)

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
