from PyQt5.QtCore import QTimerEvent
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QWidget


class Game(QMainWindow):
    def __init__(self, parent: QWidget | None, ups: int = None):
        super().__init__(parent)
        self.setupUi(self)
        if ups:
            self.update_timer_id: int = self.startTimer(ups)
            self.delta = ups

    def on_update(self, delta: int) -> None:
        pass

    def get_name(self) -> str:
        return ''

    def timerEvent(self, e: QTimerEvent) -> None:
        self.on_update(self.delta)
        self.update()

    def closeEvent(self, e: QCloseEvent) -> None:
        print('Window Closed')
        self.killTimer(self.update_timer_id)
        e.accept()
