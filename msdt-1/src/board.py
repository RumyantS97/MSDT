import random
import sqlite3

import pymorphy3

from src.data_types import WordInputOperation
from src.game_settings import LETTERS_PER_HAND, GRID_SIZE
from src.tile_types import STARTING_CELL
from src.tile_types import DEFAULT_CELL, LETTER_TIMES_TWO_CELL, LETTER_TIMES_THREE_CELL, WORD_TIMES_TWO_CELL, \
    WORD_TIMES_THREE_CELL

BOOSTERS_CONFIG_FILE = 'res/boosters.txt'
LETTER_DB_FILE = 'res/letters.db'


def get_x(x, offset, hor):
    if hor:
        return x + offset
    else:
        return x


def get_y(y, offset, hor):
    if hor:
        return y
    else:
        return y + offset


class Board:
    def __init__(self, log):
        self.let_con = sqlite3.connect(LETTER_DB_FILE)
        self.morph = pymorphy3.MorphAnalyzer()
        self.words = []
        self.log = log
        self.boosters = {}
        with open(BOOSTERS_CONFIG_FILE) as f:
            for i, line in enumerate(f.readlines()):
                for j, boost in enumerate(line.split()):
                    if boost != DEFAULT_CELL:
                        self.boosters[j, i] = int(boost)

    def generate(self):
        self.grid = [[''] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.chips = []
        cur = self.let_con.cursor()
        for i in cur.execute('''SELECT * FROM letters''').fetchall():
            for j in range(i[2]):
                self.chips.append(i[1])
        self.chips = random.sample(self.chips, len(self.chips))

    def take_chip(self):
        return self.chips.pop(-1)

    def next_chips(self):
        if len(self.chips) < LETTERS_PER_HAND:
            self.curr_chips = [''] * LETTERS_PER_HAND
        else:
            self.curr_chips = [self.take_chip() for _ in range(LETTERS_PER_HAND)]

    def update_chips(self, btns):
        for i, btn in zip(self.curr_chips, btns):
            btn.setText(i)
            if i != '':
                btn.setToolTip(f'Очков за букву: {self.get_letter_value(i)}')
            else:
                btn.setToolTip('')

    def get_letter_value(self, let):
        cur = self.let_con.cursor()
        point = cur.execute(f'''SELECT value FROM letters WHERE char='{let}' ''')
        for j in point:
            return j[0]

    def update_grid(self, btns):
        for i, j in zip(self.grid, btns):
            for let, btn in zip(i, j):
                if let != '':
                    btn.stat = True
                    btn.setEnabled(False)
                btn.setText(let)

    def update_boosters(self, btns):
        for i, line in enumerate(btns):
            for j, btn in enumerate(line):
                btn.setProperty('boost', self.boosters.get((i, j), DEFAULT_CELL))

    def commit_grid(self, btns, chips):
        for i, line in enumerate(btns):
            for j, btn in enumerate(line):
                self.grid[i][j] = btn.text()
        for i, chip in enumerate(chips):
            self.curr_chips[i] = chip.text()

    def raise_chips(self, btns, cursor):
        for i in btns:
            if i.text() != '':
                self.chips.append(i.text())
                print(i.text())
        if cursor != '':
            self.chips.append(cursor)
            print(cursor)
        self.chips = random.sample(self.chips, len(self.chips))

    def input_word(self, btns, info: WordInputOperation, fist_word):
        res = ''
        intersect = False
        for i in range(info.word_length):
            b = btns[get_x(info.start_cell_x, i, info.is_horizontal)][get_y(info.start_cell_y, i, info.is_horizontal)]
            if not fist_word and b.stat:
                intersect = True
            if fist_word and self.boosters.get(
                    (get_x(info.start_cell_x, i, info.is_horizontal), get_y(info.start_cell_y, i, info.is_horizontal)),
                    0) == STARTING_CELL:
                intersect = True
            let = b.text()
            if let == '':
                self.log('Empty Space')
                return False
            res += let
        if res in self.words:
            self.log('Word already been!!!')
            return False
        self.words.append(res)
        if not intersect:
            self.log('Слово не пересекается с предыдущими.')
            return False
        return self.check_word(res)

    def word_points(self, info: WordInputOperation):
        res = 0
        cur = self.let_con.cursor()
        post_boost = []
        for i in range(info.word_length):
            if info.is_horizontal:
                res += self.point_boost(info.start_cell_x + i, info.start_cell_y, cur, post_boost)
            else:
                res += self.point_boost(info.start_cell_x, info.start_cell_y + i, cur, post_boost)
        bonus = 0
        for i in post_boost:
            if i == WORD_TIMES_TWO_CELL:
                bonus += res
            if i == WORD_TIMES_THREE_CELL:
                bonus += res * 2
        print(f'Bonus: {bonus}')
        return res + bonus

    def point_boost(self, x, y, cur, post_boost):
        boost = self.boosters.get((x, y), DEFAULT_CELL)
        request = cur.execute(f'''SELECT value FROM letters WHERE char='{self.grid[x][y]}' ''')
        for j in request:
            res = j[0]
        print(f'Before boost: {res}')
        if boost == DEFAULT_CELL:
            print('x1')
            return res
        if boost == LETTER_TIMES_TWO_CELL:
            print('x2')
            return res * 2
        if boost == LETTER_TIMES_THREE_CELL:
            print('x3')
            return res * 3
        if boost == WORD_TIMES_TWO_CELL or boost == WORD_TIMES_THREE_CELL:
            post_boost.append(boost)
        return res

    def close(self):
        self.let_con.close()

    def check_word(self, word):
        res = self.morph.parse(word)
        for i in res:
            if {'NOUN'} in i.tag and i.normal_form.lower().replace('ё', 'е') == word:
                return True
            else:
                print(f'Incorrect tags: {i}')
        print('--------------')
        return False
