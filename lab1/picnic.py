import os

import matplotlib.pyplot as plt
import numpy as np


def save(name='', format_file='png'):
    pwd = os.getcwd()
    iPath = './pictures/{}'.format(format_file)
    if not os.path.exists(iPath):
        os.mkdir(iPath)
    os.chdir(iPath)
    plt.savefig('{}.{}'.format(name, format_file), dpi=500, format='png')
    os.chdir(pwd)


def graphic_picnic_not(p):
    if p == 0:
        y = 1
    elif p > 0 and p <= 0.2:
        y = 1 - 5 * p
    elif p > 0.2:
        y = 0
    return y


def graphic_picnic_may_be(p):
    if p < 0.4 or p > 0.6:
        y = 0
    elif p >= 0.4 and p <= 0.5:
        y = 10 * p - 4
    elif p > 0.5 and p <= 0.6:
        y = 6 - 10 * p
    return y


def graphic_picnic_yes(p):
    if p == 1:
        y = 1
    elif p < 1 and p >= 0.8:
        y = 5 * p - 4
    elif p < 0.8:
        y = 0
    return y


def draw_graph(name="pic_picnic"):
    fig = plt.figure()
    fig.set_size_inches(10, 10)
    ax = fig.add_subplot(311)
    ax2 = fig.add_subplot(312)
    ax3 = fig.add_subplot(313)
    x = np.linspace(0, 1, 1000)
    y1 = [graphic_picnic_not(x) for x in x]
    y2 = [graphic_picnic_may_be(x) for x in x]
    y3 = [graphic_picnic_yes(x) for x in x]
    ax.plot(x, y1, color="red", label="NOT")
    ax2.plot(x, y2, color="blue", label="MAYBE")
    ax3.plot(x, y3, color="green", label="YES")
    for ax in fig.axes:
        ax.set_xlabel("Вероятность, %")  # подпись у горизонтальной оси х
        ax.set_ylabel("Значение")  # подпись у вертикальной оси y
        ax.legend()  # показывать условные обозначения
    # смотри преамбулу
    save(name, format_file='pdf')
    save(name, format_file='png')
    plt.show()