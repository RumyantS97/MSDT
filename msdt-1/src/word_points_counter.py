from src.data_types import WordInputOperation
from src.letter_points_config import LetterPointsConfig
from src.tile_types import (
    DEFAULT_CELL,
    LETTER_TIMES_TWO_CELL,
    LETTER_TIMES_THREE_CELL,
    WORD_TIMES_TWO_CELL,
    WORD_TIMES_THREE_CELL,
)


class WordPointsCounter:
    def __init__(
        self,
        letter_points_config: LetterPointsConfig,
        tile_types: dict[tuple[int, int], int],
    ):
        self.letter_points_config = letter_points_config
        self.tile_types = tile_types

    def get_points_for_word(self, word: str, word_input: WordInputOperation):
        result = 0
        word_multipliers = []
        for letter, i in zip(word, range(word_input.word_length)):
            if word_input.is_horizontal:
                cell_x = word_input.start_cell_x + i
                cell_y = word_input.start_cell_y
            else:
                cell_x = word_input.start_cell_x
                cell_y = word_input.start_cell_y + i

            tile_type = self.tile_types.get((cell_x, cell_y), DEFAULT_CELL)
            points_for_letter = self.letter_points_config.get_letter_value(letter)
            if tile_type == LETTER_TIMES_TWO_CELL:
                points_for_letter *= 2
            if tile_type == LETTER_TIMES_THREE_CELL:
                points_for_letter *= 3
            if tile_type == WORD_TIMES_TWO_CELL:
                word_multipliers.append(2)
            if tile_type == WORD_TIMES_THREE_CELL:
                word_multipliers.append(3)

            result += points_for_letter

        for multiplier in word_multipliers:
            result *= multiplier

        return result
