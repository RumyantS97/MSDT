import matplotlib.pyplot as plt
import os
import numpy as np
import univers_set as uni_set
import picnic as pic


def save(name='', format_file='png'):
    pwd = os.getcwd()
    i_path = './pictures/{}'.format(format_file)
    if not os.path.exists(i_path):
        os.mkdir(i_path)
    os.chdir(i_path)
    plt.savefig('{}.{}'.format(name, format_file), dpi=500, format='png')
    os.chdir(pwd)


def defuzzification(temp, hours):
    t1 = [uni_set.weather(t) for t in temp]
    h1 = [uni_set.employment(h) for h in hours]
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


def draw_graph(temp, hours, name="pic_defuzzification"):
    fig = plt.figure()
    fig.set_size_inches(10, 10)
    ax = fig.add_subplot()
    x = np.linspace(0, 1, 1000)
    fx = []
    probability, key = defuzzification(temp, hours)
    for p, k in zip(probability, key):
        y = []
        if uni_set.KNOWLEDGE_BASE[k] == 'вероятно едем':
            G = [pic.graphic_picnic_may_be(x) for x in x]
            for g in G:
                if g < p: y.append(g)
                else: y.append(0)
        elif uni_set.KNOWLEDGE_BASE[k] == 'не едем':
            G = [pic.graphic_picnic_not(x) for x in x]
            for g in G:
                if g < p: y.append(g)
                else: y.append(0)
        elif uni_set.KNOWLEDGE_BASE[k] == 'едем':
            G = [pic.graphic_picnic_yes(x) for x in x]
            for g in G:
                if g < p: y.append(g)
                else: y.append(0)
        fx.append(y)
    fx_list = [max(p) for p in zip(fx[0], fx[1], fx[2], fx[3], fx[4], fx[5])]
    ax.plot(x, fx_list, color="blue", label="DEFUZZIFICATION")
    ax.set_xlabel("Вероятность, %")  # подпись у горизонтальной оси х
    ax.set_ylabel("Значение")  # подпись у вертикальной оси y
    ax.legend()  # показывать условные обозначения
    # смотри преамбулу
    save(name, format_file='pdf')
    save(name, format_file='png')
    plt.show()