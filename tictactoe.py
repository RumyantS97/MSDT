from tkinter import *
import random

def to_player_1(): """Игрок крестики выбирает цвет."""
    lbl_hello.destroy()
    btn_start.destroy()
    ru.title('X')

    lbl_pl1.grid(row=0, columnspan=3)

    global colour11
    colour11 = random.choice(colours_list)
    global colour12
    colour12 = random.choice(colours_list)
    global colour13
    colour13 = random.choice(colours_list)

    btn_colour_11.configure(bg=colour11)
    btn_colour_12.configure(bg=colour12)
    btn_colour_13.configure(bg=colour13)

    btn_colour_11.grid(row=1, column=0)
    btn_colour_12.grid(row=1, column=1)
    btn_colour_13.grid(row=1, column=2)

def choice1(): """Фиксирует цвет игрока крестики (1)."""
    global colour11
    global choiceof1
    choiceof1 = colour11
    to_player_2()

def choice2(): """Фиксирует цвет игрока крестики (2)."""
    global colour12
    global choiceof1
    choiceof1 = colour12
    to_player_2()

def choice3(): """Фиксирует цвет игрока крестики (3)."""
    global colour13
    global choiceof1
    choiceof1 = colour13
    to_player_2()

def to_player_2(): """Игрок нолики выбирает цвет."""
    btn_colour_11.destroy()
    btn_colour_12.destroy()
    btn_colour_13.destroy()
    ru.title('O')
    lbl_pl1.configure(text = 'Игрок Нолики, выберите цвет:')

    global colour21
    colour21 = random.choice(colours_list)
    global colour22
    colour22 = random.choice(colours_list)
    global colour23
    colour23 = random.choice(colours_list)

    btn_colour_21.configure(bg=colour21)
    btn_colour_22.configure(bg=colour22)
    btn_colour_23.configure(bg=colour23)

    btn_colour_21.grid(row=1, column=0)
    btn_colour_22.grid(row=1, column=1)
    btn_colour_23.grid(row=1, column=2)

def choice4(): """Фиксирует цвет игрока нолики (1)."""
    global colour21
    global choiceof2
    choiceof2 = colour21
    first_turn()

def choice5(): """Фиксирует цвет игрока нолики (2)."""
    global colour22
    global choiceof2
    choiceof2 = colour22
    first_turn()

def choice6(): """Фиксирует цвет игрока нолики (3)."""
    global colour23
    global choiceof2
    choiceof2 = colour23
    first_turn()

def first_turn():
    lbl_pl1.destroy()
    btn_colour_21.destroy()
    btn_colour_22.destroy()
    btn_colour_23.destroy()

    ru.title('Кто первый?')
    lbl_ft.grid(row = 0, columnspan = 3)
    btn_kr.grid(row = 1, column = 0)
    btn_rand.grid(row = 1, column = 1)
    btn_nol.grid(row = 1, column = 2)

def first_turn_kr():
    global number_of_turn
    number_of_turn = 1
    lbl_ft.destroy()
    btn_kr.destroy()
    btn_rand.destroy()
    btn_nol.destroy()
    game()

def first_turn_random():
    global number_of_turn
    number_of_turn = random.randint(1, 2)
    lbl_ft.destroy()
    btn_kr.destroy()
    btn_rand.destroy()
    btn_nol.destroy()

    if number_of_turn == 1:
        lbl_turn.configure(text = 'Первым ходит игрок Крестики')
    else:
        lbl_turn.configure(text='Первым ходит игрок Нолики')

    lbl_turn.grid(row = 0, columnspan = 3)
    btn_ok_choice.grid(row = 1, column = 1)

def to_game():
    lbl_turn.destroy()
    btn_ok_choice.destroy()
    game()

def first_turn_nol():
    global number_of_turn
    number_of_turn = 2
    lbl_ft.destroy()
    btn_kr.destroy()
    btn_rand.destroy()
    btn_nol.destroy()
    game()

def game():
    ru.title('Игра')
    btn1.grid(row=0, column=0)
    btn2.grid(row=0, column=1)
    btn3.grid(row=0, column=2)
    btn4.grid(row=1, column=0)
    btn5.grid(row=1, column=1)
    btn6.grid(row=1, column=2)
    btn7.grid(row=2, column=0)
    btn8.grid(row=2, column=1)
    btn9.grid(row=2, column=2)

    btn_verdict.grid(row = 3, column = 0)
    btn_itog.grid(row = 3, column = 1)
    btn_hooray.grid(row = 3, column = 2)

def stand1():
    global stand1_value
    matritsa(stand1_value, 1)

def stand2():
    global stand2_value
    matritsa(stand2_value, 2)

def stand3():
    global stand3_value
    matritsa(stand3_value, 3)

def stand4():
    global stand4_value
    matritsa(stand4_value, 4)

def stand5():
    global stand5_value
    matritsa(stand5_value, 5)

def stand6():
    global stand6_value
    matritsa(stand6_value, 6)

def stand7():
    global stand7_value
    matritsa(stand7_value, 7)

def stand8():
    global stand8_value
    matritsa(stand8_value, 8)

def stand9():
    global stand9_value
    matritsa(stand9_value, 9)

def matritsa(btn_value, btn_number):
    a = btn_value[0]
    b = btn_value[1]

    global pole
    if pole[a][b] != 0:  """Если клетка заполнена - пропускать."""
        pass
    else:
        global number_of_turn
        pole[a][b] = number_of_turn

        if number_of_turn == 1:
            if btn_number == 1:
                btn1.configure(text = 'x')
                btn1.configure(bg = choiceof1)
            elif btn_number == 2:
                btn2.configure(text = 'x')
                btn2.configure(bg=choiceof1)
            elif btn_number == 3:
                btn3.configure(text = 'x')
                btn3.configure(bg=choiceof1)
            elif btn_number == 4:
                btn4.configure(text = 'x')
                btn4.configure(bg=choiceof1)
            elif btn_number == 5:
                btn5.configure(text = 'x')
                btn5.configure(bg=choiceof1)
            elif btn_number == 6:
                btn6.configure(text = 'x')
                btn6.configure(bg=choiceof1)
            elif btn_number == 7:
                btn7.configure(text = 'x')
                btn7.configure(bg=choiceof1)
            elif btn_number == 8:
                btn8.configure(text = 'x')
                btn8.configure(bg=choiceof1)
            else:
                btn9.configure(text = 'x')
                btn9.configure(bg=choiceof1)

        else:
            if btn_number == 1:
                btn1.configure(text = 'o')
                btn1.configure(bg = choiceof2)
            elif btn_number == 2:
                btn2.configure(text = 'o')
                btn2.configure(bg=choiceof2)
            elif btn_number == 3:
                btn3.configure(text = 'o')
                btn3.configure(bg=choiceof2)
            elif btn_number == 4:
                btn4.configure(text = 'o')
                btn4.configure(bg=choiceof2)
            elif btn_number == 5:
                btn5.configure(text = 'o')
                btn5.configure(bg=choiceof2)
            elif btn_number == 6:
                btn6.configure(text = 'o')
                btn6.configure(bg=choiceof2)
            elif btn_number == 7:
                btn7.configure(text = 'o')
                btn7.configure(bg=choiceof2)
            elif btn_number == 8:
                btn8.configure(text = 'o')
                btn8.configure(bg=choiceof2)
            else:
                btn9.configure(text = 'o')
                btn9.configure(bg=choiceof2)

        if number_of_turn == 1:
            number_of_turn = 2
        else:
            number_of_turn = 1

    """Нужно проверить выиграл ли кто-нибудь."""
    if pole[0][0] == pole[0][1] == pole[0][2] == 1:  """Верхняя строка."""
        btn1.configure(bg='red')
        btn2.configure(bg='red')
        btn3.configure(bg='red')

        btn_itog.configure(text = 'Крестики')
        btn_again.grid(row = 4, column = 0)
        btn_quit.grid(row = 4, column = 1)
        btn_hooray.configure(text = random.choice(hooray_list))

    elif pole[0][0] == pole[0][1] == pole[0][2] == 2:
        btn1.configure(bg='red')
        btn2.configure(bg='red')
        btn3.configure(bg='red')

        btn_itog.configure(text='Нолики')
        btn_again.grid(row=4, column=0)
        btn_quit.grid(row=4, column=1)
        btn_hooray.configure(text=random.choice(hooray_list))

    elif pole[1][0] == pole[1][1] == pole[1][2] == 1: """Средняя строка."""
        btn4.configure(bg='red')
        btn5.configure(bg='red')
        btn6.configure(bg='red')

        btn_itog.configure(text='Крестики')
        btn_again.grid(row=4, column=0)
        btn_quit.grid(row=4, column=1)
        btn_hooray.configure(text=random.choice(hooray_list))
    elif pole[1][0] == pole[1][1] == pole[1][2] == 2:
        btn4.configure(bg='red')
        btn5.configure(bg='red')
        btn6.configure(bg='red')

        btn_itog.configure(text='Нолики')
        btn_again.grid(row=4, column=0)
        btn_quit.grid(row=4, column=1)
        btn_hooray.configure(text=random.choice(hooray_list))


    elif pole[2][0] == pole[2][1] == pole[2][2] == 1: """Нижняя строка."""
        btn7.configure(bg='red')
        btn8.configure(bg='red')
        btn9.configure(bg='red')

        btn_itog.configure(text='Крестики')
        btn_again.grid(row=4, column=0)
        btn_quit.grid(row=4, column=1)
        btn_hooray.configure(text=random.choice(hooray_list))
    elif pole[2][0] == pole[2][1] == pole[2][2] == 2:
        btn7.configure(bg='red')
        btn8.configure(bg='red')
        btn9.configure(bg='red')

        btn_itog.configure(text='Нолики')
        btn_again.grid(row=4, column=0)
        btn_quit.grid(row=4, column=1)
        btn_hooray.configure(text=random.choice(hooray_list))

        ################################################
    elif pole[0][0] == pole[1][0] == pole[2][0] == 1:  """Левый столбец."""
        btn1.configure(bg='red')
        btn4.configure(bg='red')
        btn7.configure(bg='red')

        btn_itog.configure(text='Крестики')
        btn_again.grid(row=4, column=0)
        btn_quit.grid(row=4, column=1)
        btn_hooray.configure(text=random.choice(hooray_list))
    elif pole[0][0] == pole[1][0] == pole[2][0] == 2:
        btn1.configure(bg='red')
        btn4.configure(bg='red')
        btn7.configure(bg='red')

        btn_itog.configure(text='Нолики')
        btn_again.grid(row=4, column=0)
        btn_quit.grid(row=4, column=1)
        btn_hooray.configure(text=random.choice(hooray_list))

    elif pole[0][1] == pole[1][1] == pole[2][1] == 1:  """Средний столбец."""
        btn2.configure(bg='red')
        btn5.configure(bg='red')
        btn8.configure(bg='red')

        btn_itog.configure(text='Крестики')
        btn_again.grid(row=4, column=0)
        btn_quit.grid(row=4, column=1)
        btn_hooray.configure(text=random.choice(hooray_list))
    elif pole[0][1] == pole[1][1] == pole[2][1] == 2:
        btn2.configure(bg='red')
        btn5.configure(bg='red')
        btn8.configure(bg='red')

        btn_itog.configure(text='Нолики')
        btn_again.grid(row=4, column=0)
        btn_quit.grid(row=4, column=1)
        btn_hooray.configure(text=random.choice(hooray_list))


    elif pole[0][2] == pole[1][2] == pole[2][2] == 1:  """Правый столбец."""
        btn3.configure(bg='red')
        btn6.configure(bg='red')
        btn9.configure(bg='red')

        btn_itog.configure(text='Крестики')
        btn_again.grid(row=4, column=0)
        btn_quit.grid(row=4, column=1)
        btn_hooray.configure(text=random.choice(hooray_list))
    elif pole[0][2] == pole[1][2] == pole[2][2] == 2:
        btn3.configure(bg='red')
        btn6.configure(bg='red')
        btn9.configure(bg='red')

        btn_itog.configure(text='Нолики')
        btn_again.grid(row=4, column=0)
        btn_quit.grid(row=4, column=1)
        btn_hooray.configure(text=random.choice(hooray_list))

    ##################################################
    elif pole[0][0] == pole[1][1] == pole[2][2] == 1:  """Первая диагональ."""
        btn1.configure(bg='red')
        btn5.configure(bg='red')
        btn9.configure(bg='red')

        btn_itog.configure(text='Крестики')
        btn_again.grid(row=4, column=0)
        btn_quit.grid(row=4, column=1)
        btn_hooray.configure(text=random.choice(hooray_list))
    elif pole[0][0] == pole[1][1] == pole[2][2] == 2:
        btn1.configure(bg='red')
        btn5.configure(bg='red')
        btn9.configure(bg='red')

        btn_itog.configure(text='Нолики')
        btn_again.grid(row=4, column=0)
        btn_quit.grid(row=4, column=1)
        btn_hooray.configure(text=random.choice(hooray_list))

    elif pole[2][0] == pole[1][1] == pole[0][2] == 1:  """Вторая диагональ."""
        btn7.configure(bg='red')
        btn5.configure(bg='red')
        btn3.configure(bg='red')

        btn_itog.configure(text='Крестики')
        btn_again.grid(row=4, column=0)
        btn_quit.grid(row=4, column=1)
        btn_hooray.configure(text=random.choice(hooray_list))
    elif pole[2][0] == pole[1][1] == pole[0][2] == 2:
        btn7.configure(bg='red')
        btn5.configure(bg='red')
        btn3.configure(bg='red')

        btn_itog.configure(text='Нолики')
        btn_again.grid(row=4, column=0)
        btn_quit.grid(row=4, column=1)
        btn_hooray.configure(text=random.choice(hooray_list))

    elif pole[0][0] != 0 and pole[0][1] != 0 and pole[0][2] != 0 and pole[1][0] != 0 and pole[1][1] != 0 and pole[1][2] != 0 and pole[2][0] != 0 and pole[2][1] != 0 and pole[2][2] != 0:
        btn_itog.configure(text='Ничья')
        btn_again.grid(row=4, column=0)
        btn_quit.grid(row=4, column=1)
        btn_hooray.configure(text='Эх...')

def again():
    pass

def quit():
    ru.destroy()

ru = Tk()

ru.title('Добро пожаловать!')
ru.geometry('240x339')
lbl_hello = Label(ru, text = 'Халлоу!')
lbl_hello.grid(row = 0, column = 0)
btn_start = Button(text = 'Начать', command = to_player_1)
btn_start.grid(row = 1, column = 0)

lbl_pl1 = Label(ru, text = 'Игрок КРЕСТИКИ, выберите цвет:')
btn_colour_11 = Button(ru, text = '', bg = 'magenta', command = choice1)
btn_colour_12 = Button(ru, text = '', bg = 'magenta', command = choice2)
btn_colour_13 = Button(ru, text = '', bg = 'magenta', command = choice3)

btn_colour_21 = Button(ru, text = '', bg = 'magenta', command = choice4)
btn_colour_22 = Button(ru, text = '', bg = 'magenta', command = choice5)
btn_colour_23 = Button(ru, text = '', bg = 'magenta', command = choice6)

lbl_ft = Label(ru, text = 'Кто ходит первым?')
btn_kr = Button(ru, text = 'X', command = first_turn_kr)
btn_rand = Button(ru, text = 'random', command = first_turn_random)
btn_nol = Button(ru, text = 'O', command = first_turn_nol)

lbl_turn = Label(ru, text = 'Первый игрок -')
btn_ok_choice = Button(ru, text = 'РћРљ', command = to_game)

btn1 = Button(text = 'Поставить', width = 10, height = 5, command = stand1)
btn2 = Button(text = 'Поставить', width = 10, height = 5, command = stand2)
btn3 = Button(text = 'Поставить', width = 10, height = 5, command = stand3)
btn4 = Button(text = 'Поставить', width = 10, height = 5, command = stand4)
btn5 = Button(text = 'Поставить', width = 10, height = 5, command = stand5)
btn6 = Button(text = 'Поставить', width = 10, height = 5, command = stand6)
btn7 = Button(text = 'Поставить', width = 10, height = 5, command = stand7)
btn8 = Button(text = 'Поставить', width = 10, height = 5, command = stand8)
btn9 = Button(text = 'Поставить', width = 10, height = 5, command = stand9)

btn_verdict = Button(text = 'Вердикт:', width = 10, height = 2)
btn_itog = Button(text = '', width = 10, height = 2)
btn_hooray = Button(text = '', width = 10, height = 2)
btn_again = Button(ru, text = 'Сыграть снова', width = 10, height = 2, command = again)
btn_quit = Button(ru, text = 'Выйти', width = 10, height = 2, command = quit)

"""Выбор цвета"""
colour11 = ''
colour12 = ''
colour13 = ''
choiceof1 = ''

colour21 = ''
colour22 = ''
colour23 = ''
choiceof2 = ''

number_of_turn = 0

pole = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

stand1_value = [0, 0]
stand2_value = [0, 1]
stand3_value = [0, 2]
stand4_value = [1, 0]
stand5_value = [1, 1]
stand6_value = [1, 2]
stand7_value = [2, 0]
stand8_value = [2, 1]
stand9_value = [2, 2]

colours_list =['blanched almond', 'bisque', 'peach puff', 'navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender','lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray', 'light slate gray', 'gray', 'light grey', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue','slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue', 'blue','dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue', 'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise', 'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green', 'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green', 'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green', 'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow', 'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown', 'indian red', 'saddle brown', 'sandy brown', 'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange', 'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink', 'pale violet red', 'maroon', 'medium violet red', 'violet red', 'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple', 'thistle', 'snow2', 'snow3', 'snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2', 'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2', 'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4', 'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3', 'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4', 'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3','MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3', 'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4', 'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2', 'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4', 'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2', 'LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3', 'SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3', 'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4', 'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2', 'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3', 'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3', 'cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4', 'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3', 'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2', 'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4', 'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4', 'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2', 'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4', 'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4', 'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4', 'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4', 'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4', 'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2', 'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1', 'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1', 'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2', 'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2', 'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2', 'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4',  'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2', 'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4', 'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4', 'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1',  'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2',  'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4', 'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1', 'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3', 'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4', 'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2', 'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4', 'gray1', 'gray2', 'gray3', 'gray4', 'gray5', 'gray6', 'gray7', 'gray8', 'gray9', 'gray10', 'gray11', 'gray12', 'gray13', 'gray14', 'gray15', 'gray16', 'gray17', 'gray18', 'gray19', 'gray20', 'gray21', 'gray22', 'gray23', 'gray24', 'gray25', 'gray26', 'gray27', 'gray28', 'gray29', 'gray30', 'gray31', 'gray32', 'gray33', 'gray34', 'gray35', 'gray36', 'gray37', 'gray38', 'gray39', 'gray40', 'gray42', 'gray43', 'gray44', 'gray45', 'gray46', 'gray47', 'gray48', 'gray49', 'gray50', 'gray51', 'gray52', 'gray53', 'gray54', 'gray55', 'gray56',  'gray57', 'gray58', 'gray59', 'gray60', 'gray61', 'gray62', 'gray63', 'gray64', 'gray65',  'gray66', 'gray67', 'gray68', 'gray69', 'gray70', 'gray71', 'gray72', 'gray73', 'gray74', 'gray75', 'gray76', 'gray77', 'gray78', 'gray79', 'gray80', 'gray81', 'gray82', 'gray83', 'gray84', 'gray85', 'gray86', 'gray87', 'gray88', 'gray89', 'gray90', 'gray91', 'gray92', 'gray93', 'gray94', 'gray95', 'gray97', 'gray98', 'gray99']
random.shuffle(colours_list)

hooray_list = ['Ура!', 'Победа!', 'Поздравляем!', 'Браво!', 'Отлично!', 'Так держать!']
random.shuffle(hooray_list)

ru.mainloop()