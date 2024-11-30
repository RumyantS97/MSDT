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
    """
    Performs linear interpolation between two values.

    :param a: The first value.
    :param b: The second value.
    :param t: The interpolation coefficient (between 0 and 1).
    :return: The interpolated value.
    """
    return a + (b - a) * t


def calculate_march_squares_2d(field: Callable[[float, float], float],
                               min_bound: Vector2 = MIN_BOUND,
                               max_bound: Vector2 = MAX_BOUND,
                               march_resolution: Vector2Int = MARCH_RESOLUTION,
                               threshold: float = THRESHOLD) -> List[Section]:
    """
    Calculates contour lines of an implicitly defined function f(x, y) = 0 using the marching squares method.

    :param field: The function defining the field of values.
    :param min_bound: The minimum bounds of the region.
    :param max_bound: The maximum bounds of the region.
    :param march_resolution: The resolution of the grid.
    :param threshold: The threshold value.
    :return: A list of line segments approximating the contour lines.
    """
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
        # Interpolation
        a = get_interpolated_point(col, col + dx, row, a_val, b_val, threshold)
        b = get_interpolated_point(col, col + dx, row, b_val, c_val, threshold)
        c = get_interpolated_point(col, col + dx, row, d_val, c_val, threshold)
        d = get_interpolated_point(col, col + dx, row, a_val, d_val, threshold)
        # Without interpolation
        # a = (col + dx * 0.5, row           )
        # b = (col + dx,       row + dy * 0.5)
        # c = (col + dx * 0.5, row + dy      )
        # d = (col,            row + dy * 0.5)

        sections.extend(get_sections_from_state(state, a, b, c, d))

    return sections


def get_interpolated_point(x1, x2, y, val1, val2, threshold):
    """
    Calculates the interpolated point on a segment.

    :param x1: x-coordinate of the first point.
    :param x2: x-coordinate of the second point.
    :param y: y-coordinate of both points.
    :param val1: field value at the first point.
    :param val2: field value at the second point.
    :param threshold: threshold value.
    :return: The interpolated point (x, y).
    """
    delta_t = val2 - val1
    if abs(delta_t) < ACCURACY:
        t = np.sign(threshold - val1)
    else:
        t = (threshold - val1) / delta_t
    return (perform_linear_interpolation(x1, x2, t), y)


def get_sections_from_state(state: int, a: Vector2, b: Vector2, c: Vector2, d: Vector2) -> List[Section]:
    """
    Returns a list of segments depending on the state of the marching squares cell.

    :param state: The state of the cell.
    :param a, b, c, d: The coordinates of the cell vertices.
    :return: A list of segments.
    """
    segment_map = {
        1:  [(c, d)],
        2:  [(b, c)],
        3:  [(b, d)],
        4:  [(a, b)],
        5:  [(a, d), (b, c)],
        6:  [(a, c)],
        7:  [(a, d)],
        8:  [(a, d)],
        9:  [(a, c)],
        10: [(a, b), (c, d)],
        11: [(a, b)],
        12: [(b, d)],
        13: [(b, c)],
        14: [(c, d)],
    }
    return segment_map.get(state, [])  # Return empty list if state not found


def generate_random_value_in_range(rand_range: Union[float, Tuple[float, float]] = 1.0) -> float:
    """
    Generates a random number within a given range.

    :param rand_range: The range of values (a number or a tuple).
    :return: A random number.
    """
    if isinstance(rand_range, float):
        return random.uniform(-0.5 * rand_range, 0.5 * rand_range)
    if isinstance(rand_range, tuple):
        return random.uniform(rand_range[0], rand_range[1])
    return random.uniform(-0.5, 0.5)


def calculate_ellipsoid(x: float, y: float, parameters: Tuple[float, float, float, float, float]) -> float:
    """
    Calculates the value of the ellipsoid function.

    :param x: The x-coordinate.
    :param y: The y-coordinate.
    :param parameters: The parameters of the ellipsoid.
    :return: The value of the ellipsoid function.
    """
    return x * parameters[0] + y * parameters[1] + x * y * parameters[2] + x * x * parameters[3] + y * y * parameters[4] - 1


def generate_log_reg_ellipsoid_test_data(parameters: Tuple[float, float, float, float, float],
                                         arg_range: float = ARG_RANGE, rand_range: float = RAND_RANGE,
                                         n_points: int = N_POINTS) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generates test data for logistic regression based on an ellipsoid.

    :param parameters: The parameters of the ellipsoid.
    :param arg_range: The range of values for x and y coordinates.
    :param rand_range: The range of random noise.
    :param n_points: The number of data points.
    :return: The feature array and the target variable array.
    """
    if DEBUG_MODE:
        print(f"logistic regression f(x, y) = {parameters[0]:1.3}x + {parameters[1]:1.3}y + {parameters[2]:1.3}xy +"
              f"{parameters[3]:1.3}x^2 + {parameters[4]:1.3}y^2 - 1,\n"
              f"arg_range =  [{-arg_range * 0.5:1.3}, {arg_range * 0.5:1.3}],\n"
              f"rand_range = [{-rand_range * 0.5:1.3}, {rand_range * 0.5:1.3}]")
    features = np.zeros((n_points, 5), dtype=float)
    features[:, 0] = np.array([generate_random_value_in_range(arg_range) for _ in range(n_points)])
    features[:, 1] = np.array([generate_random_value_in_range(arg_range) for _ in range(n_points)])
    features[:, 2] = features[:, 0] * features[:, 1]
    features[:, 3] = features[:, 0] ** 2
    features[:, 4] = features[:, 1] ** 2
    groups = np.array([np.sign(calculate_ellipsoid(features[i, 0], features[i, 1], parameters)) * 0.5 + 0.5
                       for i in range(n_points)])
    return features, groups


def generate_log_reg_test_data(k: float = -1.5, b: float = 0.1, arg_range: float = 1.0,
                               rand_range: float = 0.0, n_points: int = N_POINTS) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generates test data for logistic regression.

    :param k: The slope of the line.
    :param b: The y-intercept of the line.
    :param arg_range: The range of values for x and y coordinates.
    :param rand_range: The range of random noise.
    :param n_points: The number of data points.
    :return: The feature array and the target variable array.
    """
    if DEBUG_MODE:
        print(f"logistic regression test data b = {b:1.3}, k = {k:1.3},\n"
              f"arg_range = [{-arg_range * 0.5:1.3}, {arg_range * 0.5:1.3}],\n"
              f"rand_range = [{-rand_range * 0.5:1.3}, {rand_range * 0.5:1.3}]")
    features = np.zeros((n_points, 2), dtype=float)
    features[:, 0] = np.array([generate_random_value_in_range(arg_range) for _ in range(n_points)])
    features[:, 1] = np.array([generate_random_value_in_range(arg_range) for _ in range(n_points)])
    groups = np.array([1 if features[i, 0] * k + b > features[i, 1] + generate_random_value_in_range(rand_range)
                       else 0.0 for i in range(n_points)])
    return features, groups


def calculate_sigmoid(x: np.ndarray) -> np.ndarray:
    """
    Calculates the sigmoid function.

    :param x: The input array of values.
    :return: The array of sigmoid values.
    """
    x = np.clip(x, -500, 500)
    return 1.0 / (1.0 + np.exp(-x))


def calculate_loss(group_probabilities: np.ndarray, groups: np.ndarray) -> float:
    """
    Calculates the loss function.

    :param group_probabilities: The probabilities of belonging to groups.
    :param groups: The true values of group membership.
    :return: The value of the loss function.
    """
    group_probabilities = np.clip(group_probabilities, SMOOTHING_CONSTANT, 1.0 - SMOOTHING_CONSTANT)
    return (-groups * np.log(group_probabilities) - (1.0 - groups) * np.log(1.0 - group_probabilities)).mean()


def draw_logistic_regression_data(features: np.ndarray, groups: np.ndarray, theta: np.ndarray = None) -> None:
    """
    Visualizes logistic regression data.

    :param features: The feature array.
    :param groups: The target variable array.
    :param theta: The model parameters (weights).
    :return: None
    """
    for i in range(features.shape[0]):
        if groups[i] == 0:
            plt.plot(features[i, 0], features[i, 1], '+b')
        else:
            plt.plot(features[i, 0], features[i, 1], '*r')

    if theta is not None:
        # theta[1] * x + theta[2] * y + theta[0] * 1 = 0
        if abs(theta[2]) < ACCURACY: # Check for division by zero
            return

        b = theta[0] / abs(theta[2])
        k = theta[1] / abs(theta[2])

        x_min, x_max = features[:, 0].min(), features[:, 0].max()
        y_min, y_max = features[:, 1].min(), features[:, 1].max()

        y_max = (y_max - b) / k
        y_min = (y_min - b) / k

        if y_min < y_max:
            x_max = min(x_max, y_max)
            x_min = max(x_min, y_min)
        else:
            x_max = min(x_max, y_min)
            x_min = max(x_min, y_max)

        x = [x_min, x_max]
        y = [b + x_min * k, b + x_max * k]
        plt.plot(x, y, 'k')

    plt.show()


class LogisticRegression:
    """
    Class for implementing logistic regression.
    """
    def __init__(self, learning_rate: float = LEARNING_RATE,
                 max_iters: int = MAX_ITERS, accuracy: float = LEARNING_ACCURACY):
        """
        Initializes the model parameters.

        :param learning_rate: The learning rate.
        :param max_iters: The maximum number of iterations.
        :param accuracy: The training accuracy.
        """
        self.max_train_iterations = max_iters
        self.learning_rate = learning_rate
        self.learning_accuracy = accuracy
        self.group_features_count = 0
        self.thetas = None
        self.losses = 0.0

    def __str__(self):
        """
        Returns a JSON-compatible string with the model parameters.

        :return: A JSON string.
        """
        return f"{{\n" \
               f"\t\"group_features_count\": {self.group_features_count},\n" \
               f"\t\"max_train_iters\":      {self.max_train_iterations},\n" \
               f"\t\"learning_rate\":        {self.learning_rate},\n" \
               f"\t\"learning_accuracy\":    {self.learning_accuracy},\n" \
               f"\t\"thetas\":               [{', '.join(str(e) for e in self.thetas.flat)}],\n" \
               f"\t\"losses\":               {self.losses}\n" \
               f"}}"

    def predict(self, features: np.ndarray) -> np.ndarray:
        """
        Performs prediction based on the trained model.

        :param features: The feature array.
        :return: The array of predictions.
        """
        if features.shape[1] != self.thetas.size - 1:
            raise ValueError('Incorrect data on predicted features')
        return calculate_sigmoid(features @ self.thetas[1:] + self.thetas[0])

    def train(self, features: np.ndarray, groups: np.ndarray) -> None:
        """
        Trains the logistic regression model.

        :param features: The feature array.
        :param groups: The target variable array.
        :return: None
        """
        self.group_features_count = features.shape[1]
        self.thetas = np.array([generate_random_value_in_range(1000) for _ in range(self.group_features_count + 1)])
        x = np.hstack((np.ones((features.shape[0], 1), dtype=float), features))

        for iteration in range(self.max_train_iterations):
            previous_thetas = self.thetas.copy()
            self.thetas = self.thetas - self.learning_rate * (x.T @ (calculate_sigmoid(x @ previous_thetas) - groups))
            if (np.power(previous_thetas - self.thetas, 2.0).sum()) <= self.learning_accuracy ** 2:
                break
        self.losses = calculate_loss(self.predict(features), groups)


def run_linear_regression_test():
    """
    Runs the linear logistic regression test.
    """
    features, groups = generate_log_reg_test_data()
    logistic_regression = LogisticRegression()
    logistic_regression.train(features, groups)
    draw_logistic_regression_data(features, groups, logistic_regression.thetas)


def run_non_linear_regression_test():
    """
    Runs the non-linear logistic regression test.
    """
    features, groups = generate_log_reg_ellipsoid_test_data((0.08, -0.08, 1.6, 1.0, 1.0))
    logistic_regression = LogisticRegression()
    logistic_regression.train(features, groups)
    print(logistic_regression)

    thetas = logistic_regression.thetas

    def ellipsoid_function(x: float, y: float) -> float:
        """
        Ellipsoid function for the marching squares method.
        """
        return thetas[0] + x * thetas[1] + y * thetas[2] + x * y * thetas[3] + x * x * thetas[4] + y * y * thetas[5]

    sections = calculate_march_squares_2d(ellipsoid_function)

    for arc in sections:
        p0, p1 = arc
        plt.plot([p0[0], p1[0]], [p0[1], p1[1]], 'k')

    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    print(logistic_regression.thetas / abs(logistic_regression.thetas[0]))
    draw_logistic_regression_data(features, groups)


if __name__ == "__main__":
    run_linear_regression_test()
    run_non_linear_regression_test()
