from typing import Tuple, Callable, Union, List
import matplotlib.pyplot as plt
import numpy as np
import random

"""
Пусть есть два события связаны соотношением:
P{y=1|X} = f(z) (1)
P{y=0|X} = 1 - f(z) (2)
z = b + (X,T)
f(z)  = 1 / (1 + exp{-z})
d/dz f(z)  = z' * exp{-z} / (1 + exp{-z})^2 = z' * (1 - 1/f(z))/f(z)^2 = 
           = z' * ((1 - f(z)) * f(z)) (3)

Тогда соотношения (1) и (2):
P{y=1|X} = f(b + (X,T)) (4)
P{y=0|X} = 1 - f(b + (X,T)) (5)
Вероятность y при условии Х
P{y|X} = f(b + (X,T))^y*(1 - f(b + (X,T)))^(y-1) (6)
Условие максимального правдоподобия:
{b,T} = argmax(П P{y_i|X_i}) = argmax(Σ ln(P{y_i|X_i}))
argmax(Σ ln(P{y_i|X_i})) = Σ y_i * ln(f(b + (X,T))) + (1-y_i) * (ln(1 - f(b + (X,T))))
требуеся найти производные для:
d/db argmax(Σ ln(P{y_i|X_i}))
d/t_j argmax(Σ ln(P{y_i|X_i})), где t_j элемент вектора T
Для этого распишем необходимые нам формулы:
d/dx ln(f(x)) = af'(x)/f(x)

d/db   ln(f(b + (X,T))) =       f'(b + (X,T))/f(b + (X,T)) =        1 - f(b + (X,T) 
d/dx_j ln(f(b + (X,T))) = d/dx_j f(b + (X,T))/f(b + (X,T)) = x_j * (1 - f(b + (X,T))
"""


_debug_mode = True
_accuracy = 1e-6
Vector2Int = Tuple[int, int]
Vector2 = Tuple[float, float]
Section = Tuple[Vector2, Vector2]
EmptyArray = np.ndarray([])


def KvadratyMarsha2D(field, min_bound=(-5.0, -5.0), max_bound=(5.0, 5.0), march_resolution=(128, 128), threshold=0.5):
    def lin_interp(_a, _b, t):
        return _a + (_b - _a) * t
    rows, cols = max(march_resolution[1], 3), max(march_resolution[0], 3)
    cols_ = cols - 1
    rows_ = cols - 1
    dx = (max_bound[0] - min_bound[0]) / cols_
    dy = (max_bound[1] - min_bound[1]) / rows_
    shape = []
    for i in range(cols_ * rows_):
        state = 0
        row = (i // cols_) * dy + min_bound[1]
        col = (i % cols_) * dx + min_bound[0]
        a_val = field(col, row)
        b_val = field(col + dx, row)
        c_val = field(col + dx, row + dy)
        d_val = field(col, row + dy)
        state += 8 if a_val >= threshold else 0
        state += 4 if b_val >= threshold else 0
        state += 2 if c_val >= threshold else 0
        state += 1 if d_val >= threshold else 0
        if state == 0:
            pass
        elif state == 15:
            pass
        else:
            d_t = b_val - a_val
            # без интерполяции
            # a = (col + dx * 0.5, row)
            # b = (col + dx, row + dy * 0.5)
            # c = (col + dx * 0.5, row + dy)
            # d = (col, row + dy * 0.5)
            if np.abs(d_t) >= _accuracy:
                t_val = (threshold - a_val) / d_t
                a = (lin_interp(col, col + dx, t_val), row)
            else:
                a = (lin_interp(col, col + dx, np.sign(threshold - a_val)), row)
            d_t = c_val - b_val
            if np.abs(d_t) >= _accuracy:
                t_val = (threshold - b_val) / d_t
                b = (col + dx, lin_interp(row, row + dy, t_val))
            else:
                b = (col + dx, lin_interp(row, row + dy, np.sign(threshold - b_val)))
            d_t = c_val - d_val
            if np.abs(d_t) >= _accuracy:
                t_val = (threshold - d_val) / d_t
                c = (lin_interp(col, col + dx, t_val), row + dy)
            else:
                c = (lin_interp(col, col + dx, np.sign(threshold - d_val)), row + dy)
            d_t = d_val - a_val
            if np.abs(d_t) >= _accuracy:
                t_val = (threshold - a_val) / d_t
                d = (col, lin_interp(row, row + dy, t_val))
            else:
                d = (col, lin_interp(row, row + dy, np.sign(threshold - a_val)))

            if state == 1:
                shape.append((c, d))
            elif state == 2:
                shape.append((b, c))
            elif state == 3:
                shape.append((b, d))
            elif state == 4:
                shape.append((a, b))
            elif state == 5:
                shape.append((a, d));
                shape.append((b, c))
            elif state == 6:
                shape.append((a, c))
            elif state == 7:
                shape.append((a, d))
            elif state == 8:
                shape.append((a, d))
            elif state == 9:
                shape.append((a, c))
            elif state == 10:
                shape.append((a, b));
                shape.append((c, d))
            elif state == 11:
                shape.append((a, b))
            elif state == 12:
                shape.append((b, d))
            elif state == 13:
                shape.append((b, c))
            elif state == 14:
                shape.append((c, d))
            else:
                pass

    return shape


def ChisloVRandDiapazone(rand_range=1.0):
    if isinstance(rand_range, float):
        return random.uniform(-0.5 * rand_range, 0.5 * rand_range)
    elif isinstance(rand_range, tuple):
        return random.uniform(rand_range[0], rand_range[1])
    else:
        return random.uniform(-0.5, 0.5)


def Elipsoid(x, y, params):
    return x * params[0] + y * params[1] + x * y * params[2] + x * x * params[3] + y * y * params[4] - 1


def TestDannyeDlyaLogRegElipsoid(params, arg_range=5.0, rand_range=1.0, n_points=3000):
    if _debug_mode:
        print(f"logistic regression f(x,y) = {params[0]:1.3}x + {params[1]:1.3}y + {params[2]:1.3}xy +"
              f"{params[3]:1.3}x^2 + {params[4]:1.3}y^2 - 1,\n"
              f"arg_range =  [{-arg_range * 0.5:1.3}, {arg_range * 0.5:1.3}],\n"
              f"rand_range = [{-rand_range * 0.5:1.3}, {rand_range * 0.5:1.3}]")
    features = np.zeros((n_points, 5), dtype=float)
    features[:, 0] = np.array([ChisloVRandDiapazone(arg_range) for _ in range(n_points)])
    features[:, 1] = np.array([ChisloVRandDiapazone(arg_range) for _ in range(n_points)])
    features[:, 2] = features[:, 0] * features[:, 1]
    features[:, 3] = features[:, 0] * features[:, 0]
    features[:, 4] = features[:, 1] * features[:, 1]
    groups = np.array([np.sign(Elipsoid(features[i, 0], features[i, 1], params)) * 0.5 + 0.5 for i in range(n_points)])
    return features, groups


def TestDannyeDlyaLogReg(k=-1.5, b=0.1, arg_range=1.0, rand_range=0.0, n_points=3000):
    if _debug_mode:
        print(f"logistic regression test data b = {b:1.3}, k = {k:1.3},\n"
              f"arg_range = [{-arg_range * 0.5:1.3}, {arg_range * 0.5:1.3}],\n"
              f"rand_range = [{-rand_range * 0.5:1.3}, {rand_range * 0.5:1.3}]")
    features = np.zeros((n_points, 2), dtype=float)
    features[:, 0] = np.array([ChisloVRandDiapazone(arg_range) for _ in range(n_points)])
    features[:, 1] = np.array([ChisloVRandDiapazone(arg_range) for _ in range(n_points)])
    groups = np.array([1 if features[i, 0] * k + b > features[i, 1] + ChisloVRandDiapazone(rand_range) else 0.0 for i in
                       range(n_points)])
    return features, groups


def Sigmoida(x):
    x = np.clip(x, -500, 500)
    return 1.0 / (1.0 + np.exp(-x))


def FunktsiyaPoteri(groups_probs, groups):
    return (-groups * np.log(groups_probs) - (1.0 - groups) * np.log(1.0 - groups_probs)).mean()


def RisuemLogisticheskieDannye(features, groups, theta=None):
    [plt.plot(features[i, 0], features[i, 1], '+b') if groups[i] == 0 else plt.plot(features[i, 0], features[i, 1],
                                                                                    '*r') for i in
     range(features.shape[0] // 2)]

    if theta is None:
        plt.show()
    else:
        b = theta[0] / np.abs(theta[2])
        k = theta[1] / np.abs(theta[2])
        x_0, x_1 = features[:, 0].min(), features[:, 0].max()
        y_0, y_1 = features[:, 1].min(), features[:, 1].max()
        y_1 = (y_1 - b) / k
        y_0 = (y_0 - b) / k
        if y_0 < y_1:
            x_1 = min(x_1, y_1)
            x_0 = max(x_0, y_0)
        else:
            x_1 = min(x_1, y_0)
            x_0 = max(x_0, y_1)
        x = [x_0, x_1]
        y = [b + x_0 * k, b + x_1 * k]
        plt.plot(x, y, 'k')
        plt.show()


class LogisticheskayaRegressia:
    def __init__(self, learning_rate=1.0, max_iters=1000, accuracy=1e-2):
        # максимальное количество шагов градиентным спуском
        self._MaxTrainIters = 0
        # длина шага вдоль направления градиента
        self._LearningRate = 0
        # точность к которой мы стремимся
        self._LearningAccuracy = 0
        # колическто признаков одной группы
        self._GroupFeaturesCount = 0
        # параметры тетта (подробное описание в pdf файле)
        self._Thetas = None
        # текущее знаение функции потерь
        self._Losses = 0.0
        self.MaxTrainIters = max_iters
        self.LearningRate = learning_rate
        self.LearningAccuracy = accuracy
    def __str__(self):
        return f"{{\n" \
               f"\t\"GroupFeaturesCount\": {self.GroupFeaturesCount},\n" \
               f"\t\"MaxTrainIters\": {self.MaxTrainIters},\n" \
               f"\t\"LearningRate\": {self.LearningRate},\n" \
               f"\t\"LearningAccuracy\": {self.LearningAccuracy},\n" \
               f"\t\"Thetas\": [{', '.join(str(e) for e in self.Thetas.flat)}],\n" \
               f"\t\"Losses\": {self.Losses}\n" \
               f"}}"

    @property
    def GroupFeaturesCount(self):
        return self._GroupFeaturesCount

    @property
    def MaxTrainIters(self):
        return self._MaxTrainIters

    @MaxTrainIters.setter
    def MaxTrainIters(self, value):
        self._MaxTrainIters = min(max(value, 100), 100000)

    @property
    def LearningRate(self):
        return self._LearningRate

    @LearningRate.setter
    def LearningRate(self, value):
        self._LearningRate = min(max(value, 0.01), 1.0)

    @property
    def LearningAccuracy(self):
        return self._LearningAccuracy

    @LearningAccuracy.setter
    def LearningAccuracy(self, value):
        self._LearningAccuracy = min(max(value, 0.01), 1.0)

    @property
    def Thetas(self):
        return self._Thetas

    @property
    def Losses(self):
        return self._Losses

    def Predict(self, features):
        # проверка размерности - количество принаков группы == количество элементов в толбце
        if features.shape[1] != self.Thetas.size - 1:
            raise NameError('Неверные данные о прогнозируемых характеристиках')
        return Sigmoida(features @ self.Thetas[1::] + self.Thetas[0])

    def Train(self, features, groups):
        # проверка размерности -  количество принаков группы == количество элементов в толбце
        # реализация градиентного спуска для обучения логистической регрессии.
        # формула thetas(i) = thetas(i - 1) - learning_rate * (X^T * sigmoid(X *  thetas(i - 1)) - groups)
        # количество признаков у группы (в нашем случае их 2 - это x и y)
        self._GroupFeaturesCount = features.shape[1]
        # Инициализируются параметры модели (веса) thetas случайными значениями
        self._Thetas = np.array([ChisloVRandDiapazone(1000) for _ in range(self._GroupFeaturesCount + 1)])
        x = np.hstack((np.ones((features.shape[0], 1), dtype=float), features))
        # _thetas в нашем случае - это СТОЛБЕЦ из трех рандомных чисел
        # theta[0] * 1 + theta[1] * x + theta[2] * y = 0
        # Добавили слева столбец единиц к точкам (типо b = 1)
        x = np.hstack((np.ones((features.shape[0], 1), dtype=float), features))
        # К признакам добавляется столбец из единиц для учета свободного члена
        # Добавление столбца из единиц позволяет нам умножать его на соответствующий параметр thetas
        # Запускается цикл обучения с использованием градиентного спуска. На каждой итерации обновляются параметры модели согласно формуле градиентного спуска
        for iteration in range(self.MaxTrainIters):
            thetas = self.Thetas.copy()
            self._Thetas = self._Thetas - self.LearningRate * (x.T @ (Sigmoida(x @ thetas) - groups))
            # Проверяется условие остановки: если разница между предыдущими и текущими значениями параметров модели становится меньше заданной точности, то обучение завершается
            if (np.power(thetas - self.Thetas, 2.0).sum()) <= self.LearningAccuracy * self.LearningAccuracy: break


def TestLineynoyRegressii():
    # features - массив точек, group - массив классов (если 1, то красная типо, если 0, то точка синяя)
    # Точку характеризует x y на i-ой позиции в features и её класс на i-ой позиции в group
    features, group = TestDannyeDlyaLogReg()
    lg = LogisticheskayaRegressia()
    lg.Train(features, group)
    RisuemLogisticheskieDannye(features, group, lg.Thetas)


def TestNelineynoyRegressii():
    features, group = TestDannyeDlyaLogRegElipsoid((0.08, -0.08, 1.6, 1.0, 1.0))
    lg = LogisticheskayaRegressia()
    lg.Train(features, group)
    print(lg)
    def _ellipsoid(x, y):
        return lg.Thetas[0] + x * lg.Thetas[1] + y * lg.Thetas[2] + x * y * lg.Thetas[3] + x * x * lg.Thetas[
            4] + y * y * lg.Thetas[5]
    sections = KvadratyMarsha2D(_ellipsoid)
    for arc in sections:
        p_0, p_1 = arc
        plt.plot([p_0[0], p_1[0]], [p_0[1], p_1[1]], 'k')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    print(lg.Thetas / np.abs(lg.Thetas[0]))
    RisuemLogisticheskieDannye(features, group)


if __name__ == "__main__":
    TestLineynoyRegressii()
    TestNelineynoyRegressii()
