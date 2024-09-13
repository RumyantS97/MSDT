import sys

from PyQt5.QtGui import QColor, QFont, QCloseEvent
from PyQt5.QtWidgets import (
    QPushButton,
    QApplication,
    QListWidgetItem,
    QMessageBox,
    QTableWidgetItem,
    QWidget,
)

from board import Board
from data_types import Player, WordInputOperation
from game import Game
from game_settings import GRID_SIZE
from ui_wordmaker import Ui_MainWindow

UPDATES_PER_SECOND = 25

GREEN_COLOR = QColor(0, 255, 0)
RED_COLOR = QColor(255, 0, 0)


class WordMaker(Game, Ui_MainWindow):
    def __init__(self, parent: QWidget | None, players: list[Player] | None = None):
        super().__init__(parent, ups=UPDATES_PER_SECOND)
        print("WordMaker!")
        self.grid = []
        if players is None:
            players = [Player("1st", GREEN_COLOR), Player("2nd", RED_COLOR)]
        self.players = players
        self.c_player: int = 0
        self.curr_oper: WordInputOperation | None = None
        self.curr_letter: str | None = None
        for i in range(GRID_SIZE):
            line = []
            for j in range(GRID_SIZE):
                b = QPushButton("", self)
                b.resize(35, 35)
                b.move(i * 36 + 10, j * 36)
                b.clicked.connect(self.chip_input)
                font = QFont()
                font.setFamily("Comic Sans MS")
                font.setPointSize(12)
                b.setFont(font)
                b.setProperty("selected", False)
                b.setProperty("grid", True)
                line.append(b)
            self.grid.append(line)

        self.buttons: list[QPushButton] = [
            self.b0,
            self.b1,
            self.b2,
            self.b3,
            self.b4,
            self.b5,
            self.b6,
        ]
        for button in self.buttons:
            button.clicked.connect(self.chip_input)

        # Board
        self.board = Board(self.log)
        self.board.update_chips(self.buttons)
        self.board.update_boosters(self.grid)
        self.lock_grid()
        self.first_turn = True
        self.turn = 0

        # Events
        self.wordStart.clicked.connect(self.start_word)
        self.wordEnd.clicked.connect(self.end_word)
        self.turnEnd.clicked.connect(self.end_turn)
        self.turnCancel.clicked.connect(self.cancel_word)

        # Table
        self.tableWidget.setRowCount(len(self.players))
        self.tableWidget.setColumnCount(0)
        for i, pl in enumerate(self.players):
            item = QTableWidgetItem()
            item.setText(pl.name)
            self.tableWidget.setVerticalHeaderItem(i, item)
        with open("res/stylesheet.txt") as f:
            self.stylesheet = f.read()
        self.setStyleSheet(self.stylesheet)

    def log(self, msg: str) -> None:
        item = QListWidgetItem(msg)
        self.listWidget.addItem(item)

    def next_player(self) -> None:
        self.c_player = self.c_player + 1
        if self.c_player >= len(self.players):
            self.c_player = 0
            self.tableWidget.setColumnCount(self.turn + 1)
            for i, pl in enumerate(self.players):
                print(self.turn, i)
                self.tableWidget.setItem(
                    i, self.turn, QTableWidgetItem(str(pl.points_amount))
                )
            self.turn += 1
            if len(self.board.chips) < len(self.players) * 7:
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
        return self.players[self.c_player]

    def lock_grid(self) -> None:
        for i in self.grid:
            for j in i:
                j.setEnabled(False)

    def start_word(self) -> None:
        b = self.checkBox.isChecked()
        if (b and self.wordX.value() + self.wordLen.value() - 1 >= GRID_SIZE) or (
            not b and self.wordY.value() + self.wordLen.value() - 1 >= GRID_SIZE
        ):
            self.log("Out of bounds")
            return
        self.lock_grid()
        self.wordStart.setEnabled(False)
        self.wordEnd.setEnabled(True)
        self.turnCancel.setEnabled(True)
        self.turnEnd.setEnabled(False)
        self.curr_oper = WordInputOperation(
            self.wordX.value(), self.wordY.value(), self.wordLen.value(), b
        )
        for i in range(self.wordLen.value()):
            if b:
                cell = self.grid[self.wordX.value() + i][self.wordY.value()]
            else:
                cell = self.grid[self.wordX.value()][self.wordY.value() + i]
            cell.setEnabled(True)

    def end_word(self) -> None:
        assert self.curr_oper is not None
        if self.board.input_word(self.grid, self.curr_oper, self.first_turn):
            self.board.commit_grid(self.grid, self.buttons)
            self.board.update_grid(self.grid)
            self.get_curr_player().points_amount += self.board.word_points(
                self.curr_oper
            )
            self.log(
                f"У {self.get_curr_player().name} теперь {self.get_curr_player().points_amount} очков!"
            )
            self.lock_grid()
            self.wordStart.setEnabled(True)
            self.wordEnd.setEnabled(False)
            self.turnCancel.setEnabled(False)
            self.turnEnd.setEnabled(True)
            self.first_turn = False
        else:
            self.log("Invalid word!")

    def end_turn(self) -> None:
        previous_player_name = self.get_curr_player().name
        self.next_player()
        self.board.release_unused_chips(self.buttons, self.curr_letter)
        self.board.next_chips()
        self.board.update_chips(self.buttons)
        self.lock_grid()
        self.curr_letter = None
        self.cursorLet.setText("")
        self.log(f'Ход закончен для "{previous_player_name}".')
        self.log(f'Следующий ход для "{self.get_curr_player().name}".')

    def unlock_cell(self, x: int, y: int) -> None:
        cell = self.grid[x][y]
        cell.setEnabled(True)

    def cancel_word(self) -> None:
        self.lock_grid()
        self.board.update_grid(self.grid)
        self.board.update_chips(self.buttons)
        self.curr_oper = None
        self.curr_letter = None
        self.wordStart.setEnabled(True)
        self.wordEnd.setEnabled(False)
        self.turnCancel.setEnabled(False)
        self.turnEnd.setEnabled(True)

    def chip_input(self) -> None:
        btn: QPushButton = self.sender()  # type: ignore[assignment]
        button_letter = btn.text()
        cursor_letter = self.curr_letter
        btn.setText(cursor_letter or "")

        if button_letter != "":
            self.curr_letter = button_letter
            self.cursorLet.setText(f"Буква в руке: {self.curr_letter}")
        else:
            self.curr_letter = None
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
        for i in self.buttons:
            i.setEnabled(locked)

    def on_update(self, delta: int) -> None:
        b = self.checkBox.isChecked()
        self.checkBox.setText("→" if b else "↓")
        for buttons_row in self.grid:
            for button in buttons_row:
                button.setProperty("selected", False)
        for i in range(self.wordLen.value()):
            if b:
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


if __name__ == "__main__":
    a = QApplication(sys.argv)
    ex = WordMaker(None)
    ex.show()
    sys.exit(a.exec_())
