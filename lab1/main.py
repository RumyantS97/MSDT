import Univers_set as uni_set
import Temperature as temp
import Employment as emp
import Picnic as pic
import Defuzzification as defuzz


if __name__ == '__main__':
    temperature = list(map(float, input('Введите  6 измерений температур: ').split()))
    hour = list(map(float, input('Введите 6 измерений времени: ').split()))
    for t, h in zip(temperature, hour):
        xt, xe = uni_set.Calculation(t, h)
        print(xt, xe)
        interp = uni_set.interpretator(t, h)
        if interp == 0:
            print('Нет в базе')
        else:
            print(interp, uni_set.knowledge_base[interp])
    temp.DrawGraph()
    emp.DrawGraph()
    pic.DrawGraph()
    defuzz.DrawGraph(temperature, hour)
