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
        self.chips = self.letter_points_config.get_letters_kit()
        self.curr_chips = [self.take_chip() for _ in range(LETTERS_PER_HAND)]

    def take_chip(self) -> str:
        return self.chips.pop(-1)

    def next_chips(self) -> None:
        if len(self.chips) < LETTERS_PER_HAND:
            self.curr_chips = [""] * LETTERS_PER_HAND
        else:
            self.curr_chips = [self.take_chip() for _ in range(LETTERS_PER_HAND)]

    def update_chips(self, btns: ButtonsForHand) -> None:
        for i, btn in zip(self.curr_chips, btns):
            btn.setText(i)
            if i != "":
                btn.setToolTip(
                    f"Очков за букву: {self.letter_points_config.get_letter_value(i)}"
                )
            else:
                btn.setToolTip("")

    def update_grid(self, btns: ButtonsGrid) -> None:
        for i, j in zip(self.grid, btns):
            for let, btn in zip(i, j):
                if let != "":
                    btn.setEnabled(False)
                btn.setText(let)

    def update_boosters(self, btns: ButtonsGrid) -> None:
        for i, line in enumerate(btns):
            for j, btn in enumerate(line):
                btn.setProperty("boost", self.tile_types.get((i, j), DEFAULT_CELL))

    def commit_grid(self, btns: ButtonsGrid, chips: ButtonsForHand) -> None:
        for i, line in enumerate(btns):
            for j, btn in enumerate(line):
                self.grid[i][j] = btn.text()
        for i, chip in enumerate(chips):
            self.curr_chips[i] = chip.text()

    def release_unused_chips(self, btns: ButtonsForHand, cursor: str | None) -> None:
        for button in btns:
            if button.text() != "":
                self.chips.append(button.text())
                print(button.text())
        if cursor is not None:
            self.chips.append(cursor)
            print(cursor)
        random.shuffle(self.chips)

    def input_word(
        self, btns: ButtonsGrid, word_input: WordInputOperation, fist_word: bool
    ) -> bool:
        res = ""
        intersect = False
        for i in range(word_input.word_length):
            if word_input.is_horizontal:
                cell_x = word_input.start_cell_x + i
                cell_y = word_input.start_cell_y
            else:
                cell_x = word_input.start_cell_x
                cell_y = word_input.start_cell_y + i

            b = btns[cell_x][cell_y]
            if not fist_word:
                intersect = True
            if (
                fist_word
                and self.tile_types.get((cell_x, cell_y), DEFAULT_CELL) == STARTING_CELL
            ):
                intersect = True
            let = b.text()
            if let == "":
                self.log("Empty Space")
                return False
            res += let
        if res in self.words:
            self.log("Word already been!!!")
            return False
        self.words.append(res)
        if not intersect:
            self.log("Слово не пересекается с предыдущими.")
            return False
        return self.word_existence_checker.is_valid_word(res)

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
