import random
import sqlite3

LETTER_DB_FILE = "res/letters.db"


class LetterPointsConfig:
    def __init__(self):
        self.let_con = sqlite3.connect(LETTER_DB_FILE)

    def get_letters_kit(self) -> list[str]:
        """
        :return: Перемешанный набор букв, необходимый для выдачи игрокам
        """
        chips = []
        cur = self.let_con.cursor()
        for i in cur.execute("""SELECT * FROM letters""").fetchall():
            for j in range(i[2]):
                chips.append(i[1])
        random.shuffle(chips)
        return chips

    def get_letter_value(self, letter: str) -> int:
        """
        :param letter: Входная буква
        :return: Количество очков за букву
        """
        cur = self.let_con.cursor()
        line = cur.execute(
            f"""SELECT value FROM letters WHERE char='{letter}' """
        ).fetchone()
        return line[0]

    def close(self):
        self.let_con.close()
