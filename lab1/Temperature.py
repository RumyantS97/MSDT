import matplotlib.pyplot as plt
import os
import numpy as np


def save(name='', format='png'):
    pwd = os.getcwd()
    iPath = './pictures/{}'.format(format)
    if not os.path.exists(iPath):
        os.mkdir(iPath)
    os.chdir(iPath)
    plt.savefig('{}.{}'.format(name, format), dpi=500, format='png')
    os.chdir(pwd)


def graphicTemperatureCold(t):
    if t >= 0 and t <= 15:
        y = 1 - t / 15
    else:
        y = 0
    return y


def graphicTemperatureWarmly(t):
    if t < 15 or t > 25:
        y = 0
    elif t >= 15 and t < 17:
        y = 0.5 * t - 7.5
    elif t >= 17 and t <= 23:
        y = 1
    elif t > 23 and t <= 25:
        y = 12.5 - 0.5 * t
    return y


def graphicTemperatureHot(t):
    if t < 25:
        y = 0
    elif t >= 25 and t < 27:
        y = 0.5 * t - 12.5
    elif t >= 27:
        y = 1
    return y


def DrawGraph(name="pic_temperature"):
    fig = plt.figure()
    fig.set_size_inches(10, 10)
    ax = fig.add_subplot(311)
    ax2 = fig.add_subplot(312)
    ax3 = fig.add_subplot(313)
    x = np.linspace(0, 30, 1000)
    y1 = [graphicTemperatureCold(x) for x in x]
    y2 = [graphicTemperatureWarmly(x) for x in x]
    y3 = [graphicTemperatureHot(x) for x in x]
    ax.plot(x, y1, color="blue", label="COLD")
    ax2.plot(x, y2, color="orange", label="WARMLY")
    ax3.plot(x, y3, color="red", label="HOT")
    for ax in fig.axes:
        ax.set_xlabel("Температура, ℃")  # подпись у горизонтальной оси х
        ax.set_ylabel("Значение")  # подпись у вертикальной оси y
        ax.legend()  # показывать условные обозначения
    # смотри преамбулу
    save(name, format='pdf')
    save(name, format='png')
    plt.show()
