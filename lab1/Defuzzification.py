import matplotlib.pyplot as plt
import os
import numpy as np
import Univers_set as uni_set
import Picnic as pic


def save(name='', format='png'):
    pwd = os.getcwd()
    iPath = './pictures/{}'.format(format)
    if not os.path.exists(iPath):
        os.mkdir(iPath)
    os.chdir(iPath)
    plt.savefig('{}.{}'.format(name, format), dpi=500, format='png')
    os.chdir(pwd)


def Defuzzification(temp, hours):
    t1 = [uni_set.Xweather(t) for t in temp]
    h1 = [uni_set.Yemployment(h) for h in hours]
    i, j = 0, 0
    p = []
    key = []
    for t, h in zip(temp, hours):
        key.append(uni_set.interpretator(t, h))
        if uni_set.interpretator(t, h) == 0:
            print('Error')
        elif 'или' in uni_set.interpretator(t, h):
            p.append(max(t1[i], h1[j]))
        else:
            p.append(min(t1[i], h1[j]))
        i += 1
        j += 1
    return p, key


def DrawGraph(temp, hours, name="pic_defuzzification"):
    fig = plt.figure()
    fig.set_size_inches(10, 10)
    ax = fig.add_subplot()
    x = np.linspace(0, 1, 1000)
    fx = []
    probability, key = Defuzzification(temp, hours)
    for p, k in zip(probability, key):
        y = []
        if uni_set.knowledge_base[k] == 'вероятно едем':
            G = [pic.graphicPicnicMayBe(x) for x in x]
            for g in G:
                if g < p: y.append(g)
                else: y.append(0)
        elif uni_set.knowledge_base[k] == 'не едем':
            G = [pic.graphicPicnicNot(x) for x in x]
            for g in G:
                if g < p: y.append(g)
                else: y.append(0)
        elif uni_set.knowledge_base[k] == 'едем':
            G = [pic.graphicPicnicYes(x) for x in x]
            for g in G:
                if g < p: y.append(g)
                else: y.append(0)
        fx.append(y)
    Fx = [max(p) for p in zip(fx[0], fx[1], fx[2], fx[3], fx[4], fx[5])]
    ax.plot(x, Fx, color="blue", label="DEFUZZIFICATION")
    ax.set_xlabel("Вероятность, %")  # подпись у горизонтальной оси х
    ax.set_ylabel("Значение")  # подпись у вертикальной оси y
    ax.legend()  # показывать условные обозначения
    # смотри преамбулу
    save(name, format='pdf')
    save(name, format='png')
    plt.show()