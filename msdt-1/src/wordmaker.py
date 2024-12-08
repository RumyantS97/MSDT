import sys
from typing import TypeAlias

from PyQt5.QtGui import QCloseEvent, QColor, QFont
from PyQt5.QtWidgets import (
    QApplication,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QTableWidgetItem,
    QWidget,
)

from board import Board
from data_types import Player, WordInputOperation
from game import Game
from game_settings import GRID_SIZE, LETTERS_PER_HAND
from tile_types import DEFAULT_CELL
from ui_wordmaker import Ui_MainWindow

UPDATES_PER_SECOND = 25

GREEN_COLOR = QColor(0, 255, 0)
RED_COLOR = QColor(255, 0, 0)


ButtonsGrid: TypeAlias = list[list[QPushButton]]
ButtonsForHand: TypeAlias = list[QPushButton]


class WordMaker(Game, Ui_MainWindow):
    def __init__(self, parent: QWidget | None, players: list[Player] | None = None):
        super().__init__(parent, ups=UPDATES_PER_SECOND)
        print("WordMaker!")
        if players is None:
            players = [Player("1st", GREEN_COLOR), Player("2nd", RED_COLOR)]
        self.players = players
        self.current_player_index: int = 0
        self.current_word_input: WordInputOperation | None = None
        self.current_letter: str | None = None

        self.buttons = self.setup_hand_buttons()

        # Board
        self.board = Board(self.log)
        self.update_chips()
        self.turn = 0

        self.grid = self.setup_grip_buttons()

        # Events
        self.wordStart.clicked.connect(self.start_word)
        self.wordEnd.clicked.connect(self.end_word)
        self.turnEnd.clicked.connect(self.end_turn)
        self.turnCancel.clicked.connect(self.cancel_word)

        # Table
        self.tableWidget.setRowCount(len(self.players))
        self.tableWidget.setColumnCount(0)
        for i, player in enumerate(self.players):
            item = QTableWidgetItem()
            item.setText(player.name)
            self.tableWidget.setVerticalHeaderItem(i, item)
        with open("res/stylesheet.txt") as f:
            self.stylesheet = f.read()
        self.setStyleSheet(self.stylesheet)

    def setup_hand_buttons(self) -> ButtonsForHand:
        buttons: list[QPushButton] = [
            self.b0,
            self.b1,
            self.b2,
            self.b3,
            self.b4,
            self.b5,
            self.b6,
        ]
        for button in buttons:
            button.clicked.connect(self.chip_input)
        return buttons

    def setup_grip_buttons(self) -> ButtonsGrid:
        grid = []
        for i in range(GRID_SIZE):
            line = []
            for j in range(GRID_SIZE):
                button = QPushButton("", self)
                button.resize(35, 35)
                button.move(i * 36 + 10, j * 36)
                button.clicked.connect(self.chip_input)
                font = QFont()
                font.setFamily("Comic Sans MS")
                font.setPointSize(12)
                button.setFont(font)
                button.setProperty("selected", False)
                button.setProperty("grid", True)
                button.setProperty(
                    "boost", self.board.tile_types.get((i, j), DEFAULT_CELL)
                )
                button.setEnabled(False)
                line.append(button)
            grid.append(line)
        return grid

    def update_grid(self) -> None:
        for letter_row, buttons_row in zip(self.board.grid, self.grid):
            for letter, button in zip(letter_row, buttons_row):
                if letter != "":
                    button.setEnabled(False)
                button.setText(letter)

    def update_chips(self) -> None:
        for chip, button in zip(self.board.chips_at_hand, self.buttons):
            button.setText(chip)
            if chip != "":
                button.setToolTip(
                    f"Очков за букву: {self.board.letter_points_config.get_letter_value(chip)}"
                )
            else:
                button.setToolTip("")

    def log(self, msg: str) -> None:
        item = QListWidgetItem(msg)
        self.listWidget.addItem(item)

    def next_player(self) -> None:
        self.current_player_index = self.current_player_index + 1
        if self.current_player_index >= len(self.players):
            self.current_player_index = 0
            self.tableWidget.setColumnCount(self.turn + 1)
            for i, player in enumerate(self.players):
                print(self.turn, i)
                self.tableWidget.setItem(
                    i, self.turn, QTableWidgetItem(str(player.points_amount))
                )
            self.turn += 1
            if len(self.board.chips_bag) < len(self.players) * LETTERS_PER_HAND:
                self.game_over()

    def game_over(self) -> None:
        self.lock_grid()
        self.lock_chips()
        self.wordStart.setEnabled(False)
        self.wordEnd.setEnabled(False)
        self.turnCancel.setEnabled(False)
        self.turnEnd.setEnabled(False)
        QMessageBox.about(
            self, "Game over", "В наборе закончились фишки.\nИгра завершена."
        )

    def get_curr_player(self) -> Player:
        return self.players[self.current_player_index]

    def lock_grid(self) -> None:
        for buttons_row in self.grid:
            for button in buttons_row:
                button.setEnabled(False)

    def start_word(self) -> None:
        is_word_horizontal = self.checkBox.isChecked()
        if (
            is_word_horizontal
            and self.wordX.value() + self.wordLen.value() - 1 >= GRID_SIZE
        ) or (
            not is_word_horizontal
            and self.wordY.value() + self.wordLen.value() - 1 >= GRID_SIZE
        ):
            self.log("Out of bounds")
            return
        self.lock_grid()
        self.wordStart.setEnabled(False)
        self.wordEnd.setEnabled(True)
        self.turnCancel.setEnabled(True)
        self.turnEnd.setEnabled(False)
        self.current_word_input = WordInputOperation(
            self.wordX.value(),
            self.wordY.value(),
            self.wordLen.value(),
            is_word_horizontal,
        )
        for i in range(self.wordLen.value()):
            if is_word_horizontal:
                cell = self.grid[self.wordX.value() + i][self.wordY.value()]
            else:
                cell = self.grid[self.wordX.value()][self.wordY.value() + i]
            cell.setEnabled(True)

    def get_current_word_letters(self) -> list[str]:
        assert self.current_word_input is not None

        word_letters: list[str] = []

        for i in range(self.current_word_input.word_length):
            if self.current_word_input.is_horizontal:
                cell_x = self.current_word_input.start_cell_x + i
                cell_y = self.current_word_input.start_cell_y
            else:
                cell_x = self.current_word_input.start_cell_x
                cell_y = self.current_word_input.start_cell_y + i

            button = self.grid[cell_x][cell_y]
            word_letters.append(button.text())

        return word_letters

    def get_empty_chip_indexes(self) -> list[int]:
        return [i for i, chip in enumerate(self.buttons) if chip.text() == ""]

    def end_word(self) -> None:
        assert self.current_word_input is not None
        word_letters = self.get_current_word_letters()
        if self.board.is_word_input_correct(
            word_letters, self.current_word_input, is_first_word=(self.turn == 0)
        ):
            self.board.input_word(
                word_letters,
                self.current_word_input,
                used_chips_indexes=self.get_empty_chip_indexes(),
            )
            self.get_curr_player().points_amount += self.board.word_points(
                self.current_word_input
            )
            self.log(
                f"У {self.get_curr_player().name} теперь {self.get_curr_player().points_amount} очков!"
            )
            self.lock_grid()
            self.wordStart.setEnabled(True)
            self.wordEnd.setEnabled(False)
            self.turnCancel.setEnabled(False)
            self.turnEnd.setEnabled(True)
        else:
            self.log("Неправильный ввод")

    def get_current_chips(self) -> list[str]:
        unused_chips = []
        for button in self.buttons:
            if button.text() != "":
                unused_chips.append(button.text())
        if self.current_letter is not None:
            unused_chips.append(self.current_letter)
        return unused_chips

    def end_turn(self) -> None:
        previous_player_name = self.get_curr_player().name
        self.next_player()
        self.board.release_unused_chips(self.get_current_chips())
        self.board.next_chips()
        self.update_chips()
        self.lock_grid()
        self.current_letter = None
        self.cursorLet.setText("")
        self.log(f'Ход закончен для "{previous_player_name}".')
        self.log(f'Следующий ход для "{self.get_curr_player().name}".')

    def unlock_cell(self, x: int, y: int) -> None:
        cell = self.grid[x][y]
        cell.setEnabled(True)

    def cancel_word(self) -> None:
        self.lock_grid()
        self.update_grid()
        self.update_chips()
        self.current_word_input = None
        self.current_letter = None
        self.wordStart.setEnabled(True)
        self.wordEnd.setEnabled(False)
        self.turnCancel.setEnabled(False)
        self.turnEnd.setEnabled(True)

    def chip_input(self) -> None:
        btn: QPushButton = self.sender()  # type: ignore[assignment]
        button_letter = btn.text()
        cursor_letter = self.current_letter
        btn.setText(cursor_letter or "")

        if button_letter != "":
            self.current_letter = button_letter
            self.cursorLet.setText(f"Буква в руке: {self.current_letter}")
        else:
            self.current_letter = None
            self.cursorLet.setText("")
        if cursor_letter is not None:
            btn.setToolTip(
                f"Очков за букву: {self.board.letter_points_config.get_letter_value(cursor_letter)}"
            )
        else:
            btn.setToolTip("")

    def lock_chips(self) -> None:
        self.set_chips_unlocked(False)

    def unlock_chips(self) -> None:
        self.set_chips_unlocked(True)

    def set_chips_unlocked(self, locked: bool) -> None:
        for button in self.buttons:
            button.setEnabled(locked)

    def on_update(self, delta: int) -> None:
        is_input_horizontal = self.checkBox.isChecked()
        self.checkBox.setText("→" if is_input_horizontal else "↓")
        for buttons_row in self.grid:
            for button in buttons_row:
                button.setProperty("selected", False)
        for i in range(self.wordLen.value()):
            if is_input_horizontal:
                if self.wordX.value() + i < GRID_SIZE:
                    self.grid[self.wordX.value() + i][self.wordY.value()].setProperty(
                        "selected", True
                    )
            else:
                if self.wordY.value() + i < GRID_SIZE:
                    self.grid[self.wordX.value()][self.wordY.value() + i].setProperty(
                        "selected", True
                    )
        self.setStyleSheet(self.stylesheet)

    def closeEvent(self, e: QCloseEvent) -> None:
        self.board.close()
        Game.closeEvent(self, e)

    def get_name(self) -> str:
        return "WordMaker"


def main() -> int:
    a = QApplication(sys.argv)
    ex = WordMaker(None)
    ex.show()
    return a.exec_()


if __name__ == "__main__":
    sys.exit(main())
