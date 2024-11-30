from typing import Tuple, Callable, Union, List
import matplotlib.pyplot as plt
import numpy as np
import random

# Constants
DEBUG_MODE = True
ACCURACY = 1e-6
LEARNING_RATE = 1.0
MAX_ITERS = 1000
LEARNING_ACCURACY = 1e-2
ARG_RANGE = 5.0
RAND_RANGE = 1.0
N_POINTS = 3000
MARCH_RESOLUTION = (128, 128)
THRESHOLD = 0.5
MIN_BOUND = (-5.0, -5.0)
MAX_BOUND = (5.0, 5.0)
SMOOTHING_CONSTANT = 1e-15

Vector2Int = Tuple[int, int]
Vector2 = Tuple[float, float]
Section = Tuple[Vector2, Vector2]
EmptyArray = np.ndarray([])


def perform_linear_interpolation(a: float, b: float, t: float) -> float:
    return a + (b - a) * t

def calculate_march_squares_2d(field: Callable[[float, float], float], min_bound: Vector2 = MIN_BOUND, max_bound: Vector2 = MAX_BOUND, march_resolution: Vector2Int = MARCH_RESOLUTION, threshold: float = THRESHOLD) -> List[Section]:
    rows, cols = max(march_resolution[1], 3), max(march_resolution[0], 3)
    cols_minus_one = cols - 1
    rows_minus_one = rows - 1
    dx = (max_bound[0] - min_bound[0]) / cols_minus_one
    dy = (max_bound[1] - min_bound[1]) / rows_minus_one
    sections = []

    for i in range(cols_minus_one * rows_minus_one):
        row = (i // cols_minus_one) * dy + min_bound[1]
        col = (i % cols_minus_one) * dx + min_bound[0]

        a_val = field(col, row)
        b_val = field(col + dx, row)
        c_val = field(col + dx, row + dy)
        d_val = field(col, row + dy)

        state = 0
        state += 8 if a_val >= threshold else 0
        state += 4 if b_val >= threshold else 0
        state += 2 if c_val >= threshold else 0
        state += 1 if d_val >= threshold else 0

        if state == 0 or state == 15:
            continue
        a = get_interpolated_point(col, col + dx, row, a_val, b_val, threshold)
        b = get_interpolated_point(col, col + dx, row, b_val, c_val, threshold)
        c = get_interpolated_point(col, col + dx, row, d_val, c_val, threshold)
        d = get_interpolated_point(col, col + dx, row, a_val, d_val, threshold)
        # без интерполяции
        # a = (col + dx * 0.5, row)
        # b = (col + dx, row + dy * 0.5)
        # c = (col + dx * 0.5, row + dy)
        # d = (col, row + dy * 0.5)

        sections.extend(get_sections_from_state(state, a, b, c, d))

    return sections
def get_interpolated_point(x1, x2, y, val1, val2, threshold):
    delta_t = val2 - val1
    if abs(delta_t) < ACCURACY:
        t = np.sign(threshold - val1)
    else:
        t = (threshold - val1) / delta_t
    return (perform_linear_interpolation(x1, x2, t), y)

def get_sections_from_state(state: int, a: Vector2, b: Vector2, c: Vector2, d: Vector2) -> List[Section]:
    segment_map = {
        1: [(c, d)],
        2: [(b, c)],
        3: [(b, d)],
        4: [(a, b)],
        5: [(a, d), (b, c)],
        6: [(a, c)],
        7: [(a, d)],
        8: [(a, d)],
        9: [(a, c)],
        10: [(a, b), (c, d)],
        11: [(a, b)],
        12: [(b, d)],
        13: [(b, c)],
        14: [(c, d)],
    }
    return segment_map.get(state, [])  # Return empty list if state not found


def generate_random_value_in_range(rand_range: Union[float, Tuple[float, float]] = 1.0) -> float:
    if isinstance(rand_range, float):
        return random.uniform(-0.5 * rand_range, 0.5 * rand_range)
    elif isinstance(rand_range, tuple):
        return random.uniform(rand_range[0], rand_range[1])
    else:
        return random.uniform(-0.5, 0.5)


def calculate_ellipsoid(x: float, y: float, params: Tuple[float, float, float, float, float]) -> float:
    return x * params[0] + y * params[1] + x * y * params[2] + x * x * params[3] + y * y * params[4] - 1


def generate_log_reg_ellipsoid_test_data(
    params: Tuple[float, float, float, float, float],
    arg_range: float = 5.0,
    rand_range: float = 1.0,
    n_points: int = 3000
) -> Tuple[np.ndarray, np.ndarray]:
    if DEBUG_MODE:
        print(f"logistic regression f(x,y) = {params[0]:1.3}x + {params[1]:1.3}y + {params[2]:1.3}xy +"
              f"{params[3]:1.3}x^2 + {params[4]:1.3}y^2 - 1,\n"
              f"arg_range =  [{-arg_range * 0.5:1.3}, {arg_range * 0.5:1.3}],\n"
              f"rand_range = [{-rand_range * 0.5:1.3}, {rand_range * 0.5:1.3}]")
    features = np.zeros((n_points, 5), dtype=float)
    features[:, 0] = np.array([generate_random_value_in_range(arg_range) for _ in range(n_points)])
    features[:, 1] = np.array([generate_random_value_in_range(arg_range) for _ in range(n_points)])
    features[:, 2] = features[:, 0] * features[:, 1]
    features[:, 3] = features[:, 0] * features[:, 0]
    features[:, 4] = features[:, 1] * features[:, 1]
    groups = np.array([np.sign(calculate_ellipsoid(features[i, 0], features[i, 1], params)) * 0.5 + 0.5 for i in range(n_points)])
    return features, groups


def generate_log_reg_test_data(
    k: float = -1.5,
    b: float = 0.1,
    arg_range: float = 1.0,
    rand_range: float = 0.0,
    n_points: int = 3000
) -> Tuple[np.ndarray, np.ndarray]:
    if DEBUG_MODE:
        print(f"logistic regression test data b = {b:1.3}, k = {k:1.3},\n"
              f"arg_range = [{-arg_range * 0.5:1.3}, {arg_range * 0.5:1.3}],\n"
              f"rand_range = [{-rand_range * 0.5:1.3}, {rand_range * 0.5:1.3}]")
    features = np.zeros((n_points, 2), dtype=float)
    features[:, 0] = np.array([generate_random_value_in_range(arg_range) for _ in range(n_points)])
    features[:, 1] = np.array([generate_random_value_in_range(arg_range) for _ in range(n_points)])
    groups = np.array([1 if features[i, 0] * k + b > features[i, 1] + generate_random_value_in_range(rand_range) else 0.0 for i in
                       range(n_points)])
    return features, groups


def calculate_sigmoid(x: np.ndarray) -> np.ndarray:
    x = np.clip(x, -500, 500)
    return 1.0 / (1.0 + np.exp(-x))


def calculate_loss(groups_probs: np.ndarray, groups: np.ndarray) -> float:
    return (-groups * np.log(groups_probs) - (1.0 - groups) * np.log(1.0 - groups_probs)).mean()


def draw_logistic_regression_data(features: np.ndarray, groups: np.ndarray, theta: np.ndarray = None):
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


class LogisticRegression:
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
        self.max_train_iters = max_iters
        self.learning_rate = learning_rate
        self.learning_accuracy = accuracy
    def __str__(self):
        return f"{{\n" \
               f"\t\"GroupFeaturesCount\": {self.group_features_count},\n" \
               f"\t\"MaxTrainIters\": {self.max_train_iters},\n" \
               f"\t\"LearningRate\": {self.learning_rate},\n" \
               f"\t\"LearningAccuracy\": {self.learning_accuracy},\n" \
               f"\t\"Thetas\": [{', '.join(str(e) for e in self.thetas.flat)}],\n" \
               f"\t\"Losses\": {self.losses}\n" \
               f"}}"

    @property
    def group_features_count(self) -> int:
        return self._GroupFeaturesCount

    @property
    def max_train_iters(self) -> int:
        return self._MaxTrainIters

    @max_train_iters.setter
    def max_train_iters(self, value):
        self._MaxTrainIters = min(max(value, 100), 100000)

    @property
    def learning_rate(self) -> float:
        return self._LearningRate

    @learning_rate.setter
    def learning_rate(self, value):
        self._LearningRate = min(max(value, 0.01), 1.0)

    @property
    def learning_accuracy(self) -> float:
        return self._LearningAccuracy

    @learning_accuracy.setter
    def learning_accuracy(self, value):
        self._LearningAccuracy = min(max(value, 0.01), 1.0)

    @property
    def thetas(self) -> np.ndarray:
        return self._Thetas

    @property
    def losses(self) -> float:
        return self._Losses

    def predict(self, features: np.ndarray) -> np.ndarray:
        # проверка размерности - количество принаков группы == количество элементов в толбце
        if features.shape[1] != self.thetas.size - 1:
            raise NameError('Неверные данные о прогнозируемых характеристиках')
        return calculate_sigmoid(features @ self.thetas[1::] + self.thetas[0])

    def train(self, features: np.ndarray, groups: np.ndarray):
        # проверка размерности -  количество принаков группы == количество элементов в толбце
        # реализация градиентного спуска для обучения логистической регрессии.
        # формула thetas(i) = thetas(i - 1) - learning_rate * (X^T * sigmoid(X *  thetas(i - 1)) - groups)
        # количество признаков у группы (в нашем случае их 2 - это x и y)
        self._GroupFeaturesCount = features.shape[1]
        # Инициализируются параметры модели (веса) thetas случайными значениями
        self._Thetas = np.array([generate_random_value_in_range(1000) for _ in range(self._GroupFeaturesCount + 1)])
        x = np.hstack((np.ones((features.shape[0], 1), dtype=float), features))
        # _thetas в нашем случае - это СТОЛБЕЦ из трех рандомных чисел
        # theta[0] * 1 + theta[1] * x + theta[2] * y = 0
        # Добавили слева столбец единиц к точкам (типо b = 1)
        x = np.hstack((np.ones((features.shape[0], 1), dtype=float), features))
        # К признакам добавляется столбец из единиц для учета свободного члена
        # Добавление столбца из единиц позволяет нам умножать его на соответствующий параметр thetas
        # Запускается цикл обучения с использованием градиентного спуска. На каждой итерации обновляются параметры модели согласно формуле градиентного спуска
        for iteration in range(self.max_train_iters):
            thetas = self.thetas.copy()
            self._Thetas = self._Thetas - self.learning_rate * (x.T @ (calculate_sigmoid(x @ thetas) - groups))
            # Проверяется условие остановки: если разница между предыдущими и текущими значениями параметров модели становится меньше заданной точности, то обучение завершается
            if (np.power(thetas - self.thetas, 2.0).sum()) <= self.learning_accuracy * self.learning_accuracy: break


def run_linear_regression_test():
    # features - массив точек, group - массив классов (если 1, то красная типо, если 0, то точка синяя)
    # Точку характеризует x y на i-ой позиции в features и её класс на i-ой позиции в group
    features, group = generate_log_reg_test_data()
    lg = LogisticRegression()
    lg.train(features, group)
    draw_logistic_regression_data(features, group, lg.thetas)


def run_non_linear_regression_test():
    features, group = generate_log_reg_ellipsoid_test_data((0.08, -0.08, 1.6, 1.0, 1.0))
    lg = LogisticRegression()
    lg.train(features, group)
    print(lg)
    def _ellipsoid(x, y):
        return lg.thetas[0] + x * lg.thetas[1] + y * lg.thetas[2] + x * y * lg.thetas[3] + x * x * lg.thetas[
            4] + y * y * lg.thetas[5]
    sections = calculate_march_squares_2d(_ellipsoid)
    for arc in sections:
        p_0, p_1 = arc
        plt.plot([p_0[0], p_1[0]], [p_0[1], p_1[1]], 'k')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    print(lg.thetas / np.abs(lg.thetas[0]))
    draw_logistic_regression_data(features, group)


if __name__ == "__main__":
    run_linear_regression_test()
    run_non_linear_regression_test()
