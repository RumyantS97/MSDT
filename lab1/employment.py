import os

import matplotlib.pyplot as plt
import numpy as np


def save(name='', format_file='png'):
    pwd = os.getcwd()
    i_path = './pictures/{}'.format(format_file)
    if not os.path.exists(i_path):
        os.mkdir(i_path)
    os.chdir(i_path)
    plt.savefig('{}.{}'.format(name, format_file), dpi=500, format='png')
    os.chdir(pwd)


def graphic_employment_busy(h):
    if h == 0:
        y = 1
    else:
        y = 0
    return y


def graphic_employment_time(h):
    if h < 2 or h > 6:
        y = 0
    elif h >= 2 and h < 4:
        y = 0.5 * h - 1
    elif h >= 4 and h <= 6:
        y = 3 - 0.5 * h
    return y


def graphic_employment_free(h):
    if h < 6:
        y = 0
    elif h >= 6 and h <= 8:
        y = 0.5 * h - 3
    elif h > 8:
        y = 1
    return y


def draw_graph(name="pic_employment"):
    fig = plt.figure()
    fig.set_size_inches(10, 10)
    ax = fig.add_subplot(311)
    ax2 = fig.add_subplot(312)
    ax3 = fig.add_subplot(313)
    x = np.linspace(0, 24, 1000)
    y1 = [graphic_employment_busy(x) for x in x]
    y2 = [graphic_employment_time(x) for x in x]
    y3 = [graphic_employment_free(x) for x in x]
    ax.plot(x, y1, color="orange", label="BUSY")
    ax2.plot(x, y2, color="blue", label="TIME")
    ax3.plot(x, y3, color="green", label="FREE")
    for ax in fig.axes:
        ax.set_xlabel("Время, час")  # подпись у горизонтальной оси х
        ax.set_ylabel("Значение")  # подпись у вертикальной оси y
        ax.legend()  # показывать условные обозначения
    # смотри преамбулу
    save(name, format_file='pdf')
    save(name, format_file='png')
    plt.show()