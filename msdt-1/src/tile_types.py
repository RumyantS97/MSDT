"""Содержит типы для клеток поля"""
DEFAULT_CELL = 0
LETTER_TIMES_TWO_CELL = 1
LETTER_TIMES_THREE_CELL = 2
WORD_TIMES_TWO_CELL = 3
WORD_TIMES_THREE_CELL = 4
STARTING_CELL = 5


BOOSTERS_CONFIG_FILE = 'res/boosters.txt'


def read_tile_types() -> dict[tuple[int, int], int]:
    boosters = {}
    with open(BOOSTERS_CONFIG_FILE) as f:
        for i, line in enumerate(f.readlines()):
            for j, boost in enumerate(line.split()):
                if boost != DEFAULT_CELL:
                    boosters[j, i] = int(boost)
    return boosters
