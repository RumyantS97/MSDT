from dataclasses import dataclass

from PyQt5.QtGui import QColor


@dataclass(slots=True)
class Player:
    name: str
    color: QColor
    points_amount: int = 0


@dataclass(slots=True)
class WordInputOperation:
    start_cell_x: int
    start_cell_y: int
    word_length: int
    is_horizontal: bool
