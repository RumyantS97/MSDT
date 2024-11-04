from tkinter import *
from enum import Enum
import time
import random

class PythonSnake:  # Двигать тело змеюки в текущую сторону на 1 шаг
# При этом тело может увеличиться (add='add') в размерах или нет

    def __init__(self, window, canv_x, canv_y, canv_width, canv_height):
        self.__started = 1
        self.__spped = 10
        self.__window = window
        self.__canv_x = canv_x
        self.__canv_y = canv_y
        self.canv_width = canv_width
        self.canv_height = canv_height
        self.__snake_x = self.canv_width // 2  # Координата старта змеи
        self.__snake_y = self.canv_height // 2  # Координата старта змеи
        self.canv=Canvas(self.__window, width = self.canv_width,
                                height = self.canv_height,
                                bg = self.CONST.CANVAS_BGCOLOR.value)
        self.canv.place(x = self.__canv_x, y = self.__canv_y)
        self.create_head_food()

        self.__window.bind('<d>', self.turn_right)
        self.__window.bind('<D>', self.turn_right)
        self.__window.bind('<Right>', self.turn_right)
        self.__window.bind('<s>', self.turn_down)
        self.__window.bind('<S>', self.turn_down)
        self.__window.bind('<Down>', self.turn_down)
        self.__window.bind('<a>', self.turn_left)
        self.__window.bind('<A>', self.turn_left)
        self.__window.bind('<Left>', self.turn_left)
        self.__window.bind('<w>', self.turn_up)
        self.__window.bind('<W>', self.turn_up)
        self.__window.bind('<Up>', self.turn_up)

        self.__window.bind('<e>', self.move)
        self.__window.bind('<q>', self.pause_game)
        self.__window.bind('<Destroy>', self.pause_game)
        self.__window.bind('<plus>', self.choose_speed_key)
        self.__window.bind('<minus>', self.choose_speed_key)
        self.__window.bind('<KP_Add>', self.choose_speed_key)  # Клавиша + на боковой клаве
        self.__window.bind('<KP_Subtract>', self.choose_speed_key)  # Клавиша - на боковой клаве
        # self.__window.bind('<KeyPress>', self.speed_key)  # print(event.keysym) Вычислит нажатую клавишу
        

    class CONST(Enum):  # Список возможных направлений движения и других констант
        RIGHT = 1
        DOWN = 2
        LEFT = 3
        UP = 4
        SNAKE_HCOLOR = 'red'  # Цвет головы змейки
        SNAKE_BCOLOR = 'green'  # Цвет тела змейки
        CANVAS_BGCOLOR = '#bfcff1'  # Цвет фона холста
        SNAKE_THICKNESS = 11  # Толщина тела змейки (нечётное число)
        FOOD_THICKNESS = 15  # Толщина еды (нечётное число)
        FOOD_COLOR = '#aced95'  # Цвет тела еды
        EXPLOSIVE = 15  # Диаметр взрыва при столкновении змеи с препятствием (нечётное число)
        EXPLOSIVE_BORD = 10  # Толщина контура взрыва при столкновении змеи с препятствием
        EXPLOSIVE_BCOLOR = '#ff9999'  # Цвет тела взрыва
        EXPLOSIVE_CCOLOR = '#881a1a'  # Цвет контура взрыва


    # Обработчики клавиш изменения направления движения:
    def turn_right(self,event):
        self.__vector = self.CONST.RIGHT.value

    def turn_down(self,event):
        self.__vector = self.CONST.DOWN.value

    def turn_left(self,event):
        self.__vector = self.CONST.LEFT.value

    def turn_up(self,event):
        self.__vector = self.CONST.UP.value

    def choose_speed_key(self,event):
        # print(event.keysym)
        if event.keysym =='KP_Add' or event.keysym == 'plus' :
            self.adjust_speed('+')
        elif event.keysym =='KP_Subtract' or event.keysym == 'minus' :
            self.adjust_speed('-')

    def create_head_food(self):
        rand_vect = random.randint(1,4)
        if rand_vect == 1:
            self.__vector = self.CONST.RIGHT.value
        elif rand_vect == 2:
            self.__vector = self.CONST.DOWN.value
        elif rand_vect == 3:
            self.__vector = self.CONST.LEFT.value
        else:
            self.__vector = self.CONST.UP.value
        self.head = self.element_square(self,self.__snake_x,
                             self.__snake_y,
                             self.CONST.SNAKE_THICKNESS.value,
                             self.CONST.SNAKE_HCOLOR.value)
        self.food.add(self)
        self.body = []
        self.body.append({'id': self.head.draw(),
                        'x': self.__snake_x,
                        'y': self.__snake_y})
        self.move_forward ('add')
        self.move_forward ('add')
        self.move_forward ('add')
        self.move_forward ('add')

    def adjust_speed(self, way):
        if way == '+' and self.__spped > 1:
            self.__spped -= 1
        elif way == '-' and self.__spped < 20:
            self.__spped += 1

    def reload(self):
        self.pause_game = 'n'
        self.__started = 1
        self.__spped = 10
        self.canv.delete('all')
        del self.body
        self.body = []
        self.create_head_food()
        self.start()

    def pause_game(self, event):  # Возможность остановить змейку (пауза)
        self.pause_game = 'y'

    def move(self,event):
        if self.pause_game!= 'n':
            self.start()

    def start(self):  # Бесконечный цикл движения змейки
        if self.__started == 1:
            self.pause_game = 'n'
            i = 0
            add='del'
            while i == 0:
                self.move_forward (add)
                if self.food.eat(self) == 1:
                    add='add'
                    self.adjust_speed('+')
                elif add == 'add':
                    add = 'del'
                if self.bump_wall() == 'the end':
                    break
                if self.bump_body() == 'the end':
                    break
                for x in range(1, (self.__spped + 1) ):
                    time.sleep(0.05)
                    self.__window.update()
                    if self.pause_game== 'y':
                        i = 1
                        break

    def bump_wall(self):  # Проверка на столкновение со стеной
        __head_x = self.body[-1]['x']
        __head_y = self.body[-1]['y']
        if ( (__head_x < ( (self.CONST.SNAKE_THICKNESS.value // 2) + 1 ) )
              or (__head_y < ( (self.CONST.SNAKE_THICKNESS.value // 2) + 1 ) )
              or (__head_x > ( self.canv_width
                         - (self.CONST.SNAKE_THICKNESS.value // 2) + 1) )
              or (__head_y > ( self.canv_height
                         - (self.CONST.SNAKE_THICKNESS.value // 2) +1 ) ) ):
            self.create_explosion()
            return 'the end'
        else:
            return 0

    def bump_body(self):  # Проверка на столкновение с телом змеи
        __head_x = self.body[-1]['x']
        __head_y = self.body[-1]['y']
        bump = 0
        for i in range(0,(len(self.body)-1) ):
            if ( (__head_x == self.body[i]['x'])
                  and (__head_y == self.body[i]['y']) ):
                self.create_explosion()
                bump = 'the end'
        return bump

    def create_explosion(self):
        self.__started = 0
        self.canv.create_oval( (self.body[-1]['x'] 
                               -self.CONST.EXPLOSIVE.value),
                               (self.body[-1]['y'] 
                               -self.CONST.EXPLOSIVE.value),
                               (self.body[-1]['x'] 
                               +self.CONST.EXPLOSIVE.value),
                               (self.body[-1]['y'] 
                               +self.CONST.EXPLOSIVE.value),
                               fill=self.CONST.EXPLOSIVE_BCOLOR.value,
                               outline=self.CONST.EXPLOSIVE_CCOLOR.value,
                               width=self.CONST.EXPLOSIVE_BORD.value)

    def move_forward(self, add):  # Двигать тело змеюки в текущую сторону на 1 шаг
        # При этом тело может увеличиться (add='add') в размерах или нет
        if self.__vector == self.CONST.RIGHT.value:
            deltax = self.CONST.SNAKE_THICKNESS.value
            deltay = 0
        elif self.__vector == self.CONST.DOWN.value:
            deltax = 0
            deltay = self.CONST.SNAKE_THICKNESS.value
        elif self.__vector == self.CONST.LEFT.value:
            deltax =- self.CONST.SNAKE_THICKNESS.value
            deltay = 0
        elif self.__vector == self.CONST.UP.value:
            deltax = 0
            deltay =- self.CONST.SNAKE_THICKNESS.value
        self.head.x += deltax
        self.head.y += deltay
        self.head = self.element_square(self, self.head.x, self.head.y,
                             self.CONST.SNAKE_THICKNESS.value,
                             self.CONST.SNAKE_HCOLOR.value)
        self.body.append({'id': self.head.draw(), 'x': self.head.x, 
                          'y': self.head.y})  # Создал новую голову
        self.canv.itemconfig(self.body[-2]['id'],
                             fill=self.CONST.SNAKE_BCOLOR.value)  # Перекрасил старую голову в тело
        if add!='add':
            self.canv.delete(self.body[0]['id'])
            self.body.pop(0)


    class Food:

        def add(self):
            self.Food.x = random.randint(self.CONST.FOOD_THICKNESS.value
                                     // 2, self.canv_width
                                     - self.CONST.FOOD_THICKNESS.value // 2)
            self.Food.y=random.randint(self.CONST.FOOD_THICKNESS.value 
                                     // 2, self.canv_height
                                     - self.CONST.FOOD_THICKNESS.value // 2)
            self.Food.body=self.element_square(self, self.Food.x,
                                       self.Food.y,
                                       self.CONST.FOOD_THICKNESS.value,
                                       self.CONST.FOOD_COLOR.value)
            self.Food.id=self.Food.body.draw()

        def eat(self):
            head_x=self.body[-1]['x']
            head_y=self.body[-1]['y']
            eat=0
            if ( (head_x
                     + self.CONST.SNAKE_THICKNESS.value // 2 > (self.Food.x
                                - self.CONST.FOOD_THICKNESS.value // 2) )
                     and (head_x
                     - self.CONST.SNAKE_THICKNESS.value // 2 < (self.Food.x
                                + self.CONST.FOOD_THICKNESS.value // 2) )
                     and (head_y
                     + self.CONST.SNAKE_THICKNESS.value // 2 > (self.Food.y
                                - self.CONST.FOOD_THICKNESS.value // 2) )
                     and (head_y
                     - self.CONST.SNAKE_THICKNESS.value // 2 < (self.Food.y
                                + self.CONST.FOOD_THICKNESS.value // 2) ) ):
                self.canv.delete(self.Food.id)
                self.Food.add(self)
                eat = 1
            return eat


    class Element_Square:  # Рисую квадратик со стороной d и центром x,y

        def __init__(self, self_glob, x, y, d, color):
            self.self_glob = self_glob
            self.x = x
            self.y = y
            self.d = d
            self.color = color
            if (self.d % 2) == 0:
                self.d += 1  # Сторону квадрата делаю нечётной

        def draw(self):
            x = self.x - (self.d // 2)  # Координата левой грани квадрата
            y = self.y - (self.d // 2)  # Координата верхней грани квадрата
            return self.self_glob.canv.create_rectangle(x, y, x + self.d,
                                                       y + self.d,
                                                       fill = self.color,
                                                       width = 2)


def main():
    image1_data = '''R0lGODlhSgB'''
    image2_data = '''R0lGODlhSg'''

    def button_press(a):
        reload_button['image'] = reload_button_img2
        snake.reload()

    def button_unpress(a):
        reload_button['image'] = reload_button_img1

    root = Tk()
    root.title('Программа Змейка на питоне в графике')
    root.geometry('800x600+150+150')

    frame = Frame(root, width = 740, height = 90, bg ='#f2ffe0')
    frame.place(x = 30, y = 5)
    text = Label(root, text='''Игра Змейка написана на Python 3 в ноябре 2016 года . 
                 Правила: Змейка должна кушать зелёные плоды. 
                 При съедании плода, скорость змейки возрастает. Скорость можно
                 отрегулировать вручную клавишами "+" и "-". Нельзя выползать за границы поля и есть себя.''',
                  bg = '#f2ffe0', width = 79)
    text.place(x = 30, y = 10)
    reload_button_img1 = PhotoImage(data = image1_data)
    reload_button = Label(image = reload_button_img1,bg = '#f2ffe0')
    reload_button.place(x = 675, y = 13)
    reload_button_img2 = PhotoImage(data = image2_data)
    reload_button.bind('<Button-1>', button_press)
    reload_button.bind('<ButtonRelease-1>', button_unpress)

    snake=PythonSnake(root, 30, 100, 740, 470)
    snake.start()

    root.mainloop()



if __name__ == '__main__':
    main()