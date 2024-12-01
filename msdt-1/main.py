import math
from typing import Dict, Tuple, List, Optional, Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from constants import CSV_PATH


def main() -> None:
    """
    Main function to load data, preprocess it, train a model, and evaluate performance.
    """
    data = pd.read_csv(CSV_PATH)  # loads dataset
    lb = LabelEncoder()  # instantiate the LabelEncoder class
    x = data.iloc[:, 2:32].values
    y = data["diagnosis"].values
    y = lb.fit_transform(y)  # converts the labels into ones and zeros
    x = (x-np.mean(x))/np.std(x)  # normalize the input features
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.3, random_state=0)
    x_train = x_train.T  # transposes the dataset to make matrix multiplication feasible
    x_test = x_test.T
    y_train = y_train.reshape(-1, 1)
    y_train = y_train.T
    y_test = y_test.reshape(-1, 1)
    y_test = y_test.T
    layer_dims = [x_train.shape[0], 42, 62, 12, 20, 11, 1]
    learning_rate = 1e-3
    print(f"learning_rate for training is {learning_rate}")
    print(y_test)
    parameters = network_model(x_train, y_train, x_test, y_test, learning_rate=learning_rate, epochs=10000,
                               layer_dims=layer_dims, lambd=0.0, learning_decay=0.00000001, p_keep=1.0, beta=0.9, optimizer="gradient descent")
    train_predictions = predict(x_train, parameters)
    predictions = predict(x_test, parameters)
    print(train_predictions)
    print(predictions)
    train_score = accuracy_score(train_predictions, y_train)
    print(train_score)
    score = accuracy_score(predictions, y_test)
    print(score)


def initialize_parameters(layer_dims: List[int]) -> Dict[str, np.ndarray]:
    """
    Initialize neural network parameters using He initialization.
    """
    parameters = {}
    L = len(layer_dims)
    for l in range(1, L):
        parameters[f"W{l}"] = np.random.randn(layer_dims[l], layer_dims[l-1]) * np.sqrt(
            # He weight initialization technique..By He et Al
            2/(layer_dims[l-1]))
        parameters[f"b{l}"] = np.zeros((layer_dims[l], 1))
    return parameters


def linear_forward(A: np.ndarray, W: np.ndarray, b: np.ndarray) -> Tuple[np.ndarray, Tuple[np.ndarray, np.ndarray, np.ndarray]]:
    """
    Performs the linear part of a layer's forward propagation.
    """
    Z = np.dot(W, A) + b
    cache = (A, W, b)
    return Z, cache


def sigmoid(Z: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Computes the sigmoid activation.
    """
    cache = Z
    s = 1/(1 + np.exp(-Z))
    return s, cache


def relu(Z: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Computes the ReLU activation.
    """
    s = np.maximum(0, Z)
    cache = Z
    return s, cache


def leaky_relu(Z: np.ndarray, alpha: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    Computes the leaky ReLU activation.
    """
    s = np.maximum(Z*alpha, Z)
    cache = Z
    return s, cache


def linear_activation_forward(A_prev: np.ndarray, W: np.ndarray, b: np.ndarray, activation: str) -> Tuple[np.ndarray, Tuple[Any, Any]]:
    """
    Performs the forward propagation for a single layer.
    """
    if activation == "relu":
        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = relu(Z)

    elif activation == "sigmoid":
        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = sigmoid(Z)
    cache = (linear_cache, activation_cache)
    return A, cache


def L_model_forward(X: np.ndarray, parameters: Dict[str, np.ndarray], p_keep: float = 1.0) -> Tuple[np.ndarray, List[Any], Dict[str, np.ndarray]]:
    """
    Implements forward propagation for the entire network.
    """
    caches = []
    dropout_dict = {}
    L = len(parameters) // 2
    A = X
    for i in range(1, L):
        A_prev = A
        A, cache = linear_activation_forward(
            A_prev, parameters[f"W{i}"], parameters[f"b{i}"], activation="relu")
        dropout_dict[f"D{i}"] = np.random.rand(A.shape[0], A.shape[1])
        dropout_dict[f"D{i}"] = dropout_dict[f"D{i}"] < p_keep
        A = A*dropout_dict[f"D{i}"]
        A /= p_keep
        caches.append(cache)
    AL, cache = linear_activation_forward(
        A, parameters[f"W{L}"], parameters[f"b{L}"], activation="sigmoid")
    caches.append(cache)
    return AL, caches, dropout_dict


def relu_backward(dA: np.ndarray, Z: np.ndarray) -> np.ndarray:
    """
    Computes the backward propagation for ReLU activation.
    """
    A, _ = relu(Z)
    s = (A > 0)
    dZ = dA * s
    return dZ


def sigmoid_backward(dA: np.ndarray, Z: np.ndarray) -> np.ndarray:
    """
    Computes the backward propagation for ReLU activation.
    """
    s, cache = sigmoid(Z)
    derivative = s * (1-s)
    dZ = dA * derivative
    return dZ


def linear_backward(dZ: np.ndarray, cache: Tuple[np.ndarray, np.ndarray, np.ndarray], lambd: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Performs backward propagation for the linear portion of a layer.
    """
    m = len(cache)
    linear_cache, activation_cache = cache
    A_prev, W, b = linear_cache
    Z = activation_cache
    dW = 1/m * (np.dot(dZ, A_prev.T) + (lambd*W))
    db = 1/m * np.sum(dZ, axis=1, keepdims=True)
    dA_prev = np.dot(W.T, dZ)
    return dW, db, dA_prev


def linear_backward_activation(dA: np.ndarray, cache: Tuple[Any, Any], activation: str, lambd: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Performs backward propagation for a single layer with activation.
    """
    if activation == "relu":
        linear_cache, activation_cache = cache
        Z = activation_cache
        dZ = relu_backward(dA, Z)
        dW, db, dA_prev = linear_backward(dZ, cache, lambd)
    elif activation == "sigmoid":
        linear_cache, activation_cache = cache
        Z = activation_cache
        dZ = sigmoid_backward(dA, Z)
        dW, db, dA_prev = linear_backward(dZ, cache, lambd)
    return dW, db, dA_prev


def l_model_backward(AL: np.ndarray, Y: np.ndarray, cache: List[Any], lambd: float, dropout_dict: Dict[str, np.ndarray], p_keep: float) -> Dict[str, np.ndarray]:
    """
    Implements backward propagation for the entire network.
    """
    grads = {}
    Y.shape = (AL.shape)
    dAL = -np.divide(Y, AL) + np.divide(1-Y, 1-AL+(1e-18))
    current_cache = cache[-1]
    L = len(cache)
    grads[f"dW{L}"], grads[f"db{L}"], grads[f"dA{
        L - 1}"] = linear_backward_activation(dAL, current_cache, activation="sigmoid", lambd=0.0)
    grads[f"dA{L - 1}"] = grads[f"dA{L - 1}"] * dropout_dict[f"D{L - 1}"]
    grads[f"dA{L - 1}"] /= p_keep
    for i in reversed(range(L-1)):
        current_cache = cache[i]
        grads[f"dW{i+1}"], grads[f"db{i + 1}"], grads[f"dA{i}"] = linear_backward_activation(
            grads[f"dA{i+1}"], current_cache, activation="relu", lambd=0.0)
        if i == 0:
            break
        else:
            grads[f"dA{i}"] = grads[f"dA{i}"] * dropout_dict[f"D{i}"]
            grads[f"dA{i}"] /= p_keep
    return grads


def update_parameters(parameters: Dict[str, np.ndarray], grads: Dict[str, np.ndarray], learning_rate: float) -> Dict[str, np.ndarray]:
    """
    Updates parameters using gradient descent.
    """
    L = len(parameters) // 2
    for l in range(1, L):
        parameters[f"W{l}"] = parameters[f"W{l}"] - \
            learning_rate * grads[f"dW{l}"]
        parameters[f"b{l}"] = parameters[f"b{l}"] - \
            learning_rate * grads[f"db{l}"]
    return parameters


def dict_to_vector(dictionary: Dict[str, np.ndarray]) -> Tuple[np.ndarray, np.ndarray]:
    """
    Converts a dictionary of parameters (weights and biases) to a vector.
    """
    values = []
    keys = []
    for key, value in dictionary.items():
        values.append(value)
        keys.append(key)
    new_vector = np.array(values)
    new_vector = new_vector.reshape(-1, 1)
    new_keys = np.array(keys)
    return new_vector, new_keys


def vector_to_dict(vector: np.ndarray, keys: List[str]) -> Dict[str, np.ndarray]:
    """
    Converts a vector and a list of keys back to a dictionary.
    """
    dict = {}
    for i in range(len(keys)):
        dict[keys[i]] = vector[i]
    return dict


def extract_weight(dict: Dict[str, np.ndarray]) -> List[np.ndarray]:
    """
    Extracts the weight matrices from a dictionary of parameters.
    """
    L = len(dict)//2
    values = []
    for i in range(1, L+1):
        values.append(dict["W" + str(i)])
    return values


def calc_norm(weight: List[np.ndarray]) -> float:
    """
    Computes the L2 norm (sum of squared values) of a list of weight matrices.
    """
    norm = 0
    L = len(weight)
    for i in range(L):
        norm += np.sum(np.square(weight[i]))
    return norm


def random_mini_batches(X: np.ndarray, Y: np.ndarray, mini_batch_size: int, seed: int = 0) -> List[Tuple[np.ndarray, np.ndarray]]:
    """
    Creates random mini-batches from the dataset.
    """
    mini_batch = []
    m = Y.shape[1]
    permutation = list(np.random.permutation(m))
    X_shuffled = X[:, permutation]
    Y_shuffled = Y[:, permutation].reshape(Y.shape[0], m)
    num_complete_minibatches = math.floor(m/mini_batch_size)
    for i in range(num_complete_minibatches):
        X_minibatch = X_shuffled[:, mini_batch_size*i:mini_batch_size*(i+1)]
        Y_minibatch = Y_shuffled[:, mini_batch_size*i:mini_batch_size*(i+1)]
        minibatches = (X_minibatch, Y_minibatch)
        mini_batch.append(minibatches)
    if m % mini_batch_size != 0:
        end = m - mini_batch_size * math.floor(m / mini_batch_size)
        X_minibatch = X_shuffled[:, num_complete_minibatches*mini_batch_size:]
        Y_minibatch = Y_shuffled[:, num_complete_minibatches*mini_batch_size:]
        minibatches = (X_minibatch, Y_minibatch)
        mini_batch.append(minibatches)
    return mini_batch


def initialize_velocities(params: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    """
    Initializes the velocity terms for momentum optimization.
    """
    v = {}
    L = len(params)//2
    for i in range(L):
        v[f"dW{i+1}"] = np.zeros_like(params[f"W{i+1}"])
        v[f"db{i+1}"] = np.zeros_like(params[f"b{i+1}"])
    return v


def update_parameters_with_momentum(params: Dict[str, np.ndarray],
                                    learning_rate: float,
                                    grads: Dict[str, np.ndarray],
                                    v: Dict[str, np.ndarray],
                                    beta: float
                                    ) -> Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]:
    """
    Updates parameters using gradient descent with momentum.
    """
    L = len(params)//2
    for i in range(L):
        v[f"dW{i+1}"] = beta*v[f"dW{i+1}"] + (1-beta)*grads[f"dW{i+1}"]
        v[f"db{i+1}"] = beta*v[f"db{i+1}"] + (1-beta)*grads[f"db{i+1}"]

        params[f"W{i+1}"] = params[f"W{i+1}"] - learning_rate*v[f"dW{i+1}"]
        params[f"b{i+1}"] = params[f"b{i+1}"] - learning_rate*v[f"db{i+1}"]
    return params, v


def initialize_rmsprop(params: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    """
    Initializes the RMSprop optimization variables (s) for all layers.
    """
    L = len(params)//2
    s = {}
    for l in range(L):
        s[f"dW{l+1}"] = np.zeros_like(params[f"W{l+1}"])
        s[f"db{l+1}"] = np.zeros_like(params[f"W{l+1}"])
    return s


def update_rmsprop(s: Dict[str, np.ndarray],
                   t: int,
                   params: Dict[str, np.ndarray],
                   grads: Dict[str, np.ndarray],
                   learning_rate: float,
                   beta_2: float = 0.999,
                   epsilon: float = 1e-8
                   ) -> Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]:
    """
    Updates parameters using the RMSprop optimization algorithm.
    """
    L = len(grads)//2
    s_corrected = {}
    for l in range(L):
        s[f"dW{l+1}"] = (s[f"dW{l+1}"]*beta_2) + (1-beta_2) * \
            np.square(grads[f"dW{l+1}"])
        s[f"db{l+1}"] = (s[f"db{l+1}"]*beta_2) + (1-beta_2) * \
            np.square(grads[f"db{l+1}"])
        s_corrected[f"dW{
            l+1}"] = np.divide(s[f"dW{l+1}"], 1 - np.power(beta_2, t))
        s_corrected[f"db{
            l+1}"] = np.divide(s[f"db{l+1}"], 1 - np.power(beta_2, t))
        params[f"W{l+1}"] = params[f"W{l+1}"] - \
            np.divide(learning_rate, np.sqrt(
                s_corrected[f"dW{l+1}"] + epsilon))
        params[f"b{l+1}"] = params[f"b{l+1}"] - \
            np.divide(learning_rate, np.sqrt(
                s_corrected[f"db{l+1}"] + epsilon))
    return params, s_corrected


def initialize_adam(params: Dict[str, np.ndarray]) -> Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]:
    """
    Initializes the Adam optimization variables (v and s) for all layers.
    """
    L = len(params)//2
    s = {}
    v = {}
    for l in range(L):
        v[f"dW{l+1}"] = np.zeros_like(params[f"W{l+1}"])
        v[f"db{l+1}"] = np.zeros_like(params[f"b{l+1}"])
        s[f"dW{l+1}"] = np.zeros_like(params[f"W{l+1}"])
        s[f"db{l+1}"] = np.zeros_like(params[f"b{l+1}"])
    return v, s


def update_adam(params: Dict[str, np.ndarray],
                grads: Dict[str, np.ndarray],
                v: Dict[str, np.ndarray],
                s: Dict[str, np.ndarray],
                t: int,
                learning_rate: float,
                epsilon: float = 1e-8,
                beta1: float = 0.9,
                beta2: float = 0.999
                ) -> Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray], Dict[str, np.ndarray]]:
    """
    Updates parameters using the Adam optimization algorithm.
    """
    v_corrected = {}
    s_corrected = {}
    L = len(params)//2
    for l in range(L):
        v[f"dW{l+1}"] = v[f"dW{l+1}"]*beta1 + (1-beta1)*grads[f"dW{l+1}"]
        v[f"db{l+1}"] = v[f"db{l+1}"]*beta1 + (1-beta1)*grads[f"db{l+1}"]
        v_corrected[f"dW{l+1}"] = v[f"dW{l+1}"]/(1-np.power(beta1, t))
        v_corrected[f"db{l+1}"] = v[f"db{l+1}"]/(1-np.power(beta1, t))
        s[f"dW{l+1}"] = s[f"dW{l+1}"]*beta2 + (1-beta2)*(grads[f"dW{l+1}"])**2
        s[f"db{l+1}"] = s[f"db{l+1}"]*beta2 + (1-beta2)*(grads[f"db{l+1}"])**2
        s_corrected[f"dW{l+1}"] = (s[f"dW{l+1}"])/(1 - np.power(beta2, t))
        s_corrected[f"db{l+1}"] = (s[f"db{l+1}"])/(1 - np.power(beta2, t))
        params[f"W{l+1}"] = params[f"W{l+1}"] - learning_rate * \
            np.divide(v_corrected[f"dW{l+1}"],
                      np.sqrt(s_corrected[f"dW{l+1}"]+epsilon))
        params[f"b{l+1}"] = params[f"b{l+1}"] - learning_rate * \
            np.divide(v_corrected[f"db{l+1}"],
                      np.sqrt(s_corrected[f"db{l+1}"]+epsilon))
    return params, s_corrected, v_corrected


def compute_cost(AL: np.ndarray, Y: np.ndarray, lambd: float, parameters: Dict[str, np.ndarray]) -> float:
    """
    Computes the cost function with optional L2 regularization.
    """
    L = len(parameters)//2
    m = AL.shape[1]
    weight_array = extract_weight(parameters)
    norm = calc_norm(weight_array)
    regu_term = 1/m*(lambd/2) * norm  # l2 regularization term
    cost_intial = -1/m * np.sum((Y*np.log(AL)) + (1-Y)*(np.log(1-AL)))
    cost = cost_intial + regu_term
    return cost


def network_model(x_train: np.ndarray,
                  y_train: np.ndarray,
                  x_test: np.ndarray,
                  y_test: np.ndarray,
                  learning_rate: float,
                  epochs: int,
                  layer_dims: List[int],
                  lambd: float,
                  learning_decay: float,
                  p_keep: float,
                  beta: float,
                  optimizer: Optional[str] = None) -> Dict[str, np.ndarray]:
    """
    Trains a neural network using specified parameters and optimization technique.
    """
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    parameters = initialize_parameters(layer_dims)
    t = 0
    costs = []
    cost1 = []
    scores1 = []
    scores2 = []
    v_adam, s_adam = initialize_adam(parameters)
    v_momentum = initialize_velocities(parameters)
    s_prop = initialize_rmsprop(parameters)
    for i in range(epochs):
        learning_rate = learning_rate - (learning_rate*learning_decay)
        minibatches = random_mini_batches(x_train, y_train, mini_batch_size=16)
        for mini_batch in minibatches:
            X_minibatch, Y_minibatch = mini_batch
            AL, cache, dropout_dict = L_model_forward(
                X_minibatch, parameters, p_keep)
            cost_train = compute_cost(AL, Y_minibatch, lambd, parameters)
            costs.append(cost_train)
            grads = l_model_backward(
                AL, Y_minibatch, cache, lambd, dropout_dict, p_keep)
            if optimizer is not None:

                if optimizer == "gradient descent":  # Gradient Descent
                    parameters = update_parameters(
                        parameters, grads, learning_rate)

                elif optimizer == "adam":  # Adaptive Moment Estimation Adam
                    t += 1
                    parameters, s_adam, v_adam = update_adam(
                        parameters, grads, v_adam, s_adam, t, learning_rate)

                elif optimizer == "gradient descent with momentum":  # Gradient Descent with momentum
                    parameters, v_momentum = update_parameters_with_momentum(
                        parameters, learning_rate, grads, v_momentum, beta)

                elif optimizer == "rmsprop":
                    t += 1
                    parameters, s_prop = update_rmsprop(
                        s_prop, t, parameters, grads, learning_rate)

            predictions = predict(x_train, parameters)
            score = accuracy_score(predictions, y_train)
            scores1.append(score)
        if i % 50 == 0:
            print(f"cross entropy loss after {i} th epoch = {cost_train}")
            print(f"accuracy after {i} th epoch = {score}")
            print(f"current learning_rate = {learning_rate}")
    ax1.plot(costs)
    ax2.plot(scores1, label=" training set")
    plt.legend()
    plt.show()
    return parameters


def predict(x_test: np.ndarray, parameters: Dict[str, np.ndarray]) -> np.ndarray:
    """
    Generates predictions for the test set.
    """
    predictions, _, _ = L_model_forward(x_test, parameters)
    for i in range(predictions.shape[1]):
        if predictions[0, i] >= 0.5:
            predictions[0, i] = 1
        elif predictions[0, i] < 0.5:
            predictions[0, i] = 0
    return predictions


def accuracy_score(predictions: np.ndarray, actual: np.ndarray) -> float:
    """
    Computes accuracy of the model.
    """
    counter = 0
    for i in range(predictions.shape[1]):
        if predictions[0, i] == actual[0, i]:
            counter += 1
        else:
            pass
    return counter/predictions.shape[1]


if __name__ == '__main__':
    main()
