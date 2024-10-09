import defuzzification as defuzz
import employment as emp
import picnic as pic
import temperature as temp
import univers_set as uni_set


if __name__ == '__main__':
    temperature = list(map(float, input('Введите  6 измерений температур: ').split()))
    hour = list(map(float, input('Введите 6 измерений времени: ').split()))
    for t, h in zip(temperature, hour):
        xt, xe = uni_set.calculation(t, h)
        print(xt, xe)
        interp = uni_set.interpretator(t, h)
        if interp == 0:
            print('Нет в базе')
        else:
            print(interp, uni_set.KNOWLEDGE_BASE[interp])
    temp.draw_graph()
    emp.draw_graph()
    pic.draw_graph()
    defuzz.draw_graph(temperature, hour)
