from abc import abstractmethod
from copy import deepcopy
from typing import Callable, List, Tuple
import sys
epsilon = sys.float_info.epsilon

import numpy as np

from sklearn.model_selection import KFold

from network import NeuralNetwork

try:
    from tqdm import tqdm
except ImportError:
    tqdm = lambda x: x


def train(network: NeuralNetwork, X: np.ndarray, y: np.ndarray, loss, lr: float,
          n_epochs: int, X_test: np.ndarray = None, y_test: np.ndarray = None,
          inplace: bool = True):
    """ Train a neural network using gradient descent.

    Supports train-test split, but it is not necessary.
    """
    do_test = (X_test is not None) and (y_test is not None)

    if not inplace:
        net = deepcopy(network)
    else:
        net = network

    # first loss value is from the untrained net, so the 0-th epoch
    loss_values = [loss(net(X), y)]
    if do_test:
        test_loss_values = [loss(net(X_test), y_test)]

    for _ in tqdm(list(range(n_epochs))):
        # here is where the magic happens
        net.descent_step(X, lr, loss, y)

        loss_values.append(loss(net(X), y))

        if do_test:
            test_loss_values.append(loss(net(X_test), y_test))

    if do_test:
        return net, loss_values, test_loss_values
    else:
        return net, loss_values

def train_cv(network: NeuralNetwork, X: np.ndarray, y: np.ndarray,
             loss: Callable, lr: float, n_epochs: int, k: int = 5,
             reset_weights: bool = True,
            ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, List[NeuralNetwork]]:
    kf = KFold(n_splits=k, shuffle=True)

    train_losses = list()
    test_losses = list()
    accus = list()
    nets = list()
    for train_index, test_index in tqdm(list(kf.split(X, y))):
        X_train, y_train = X[train_index], y[train_index]
        X_test, y_test = X[test_index], y[test_index]

        net = deepcopy(network)
        if reset_weights:
            net.reset_weights()

        net, train_losses_k, test_losses_k = train(net, X_train, y_train, loss,
                                                   lr, n_epochs, X_test, y_test)
        train_losses.append(train_losses_k)
        test_losses.append(test_losses_k)

        y_pred = net(X_test) > 0.5
        accus.append(np.sum(y_pred == y_test) / y_test.shape[0])

        nets.append(net)

    train_losses = np.array(train_losses)
    test_losses = np.array(test_losses)
    accus = np.array(accus)

    return train_losses, test_losses, accus, nets

class Loss():
    def __init__(self) -> None:
        pass

    @abstractmethod
    def __call__(y_pred: np.ndarray, y_true: np.ndarray) -> float:
        pass

    @abstractmethod
    def grad(y_pred: np.ndarray, y_true: np.ndarray) -> np.ndarray:
        pass

class BCE_Loss(Loss):
    def __init__(self) -> None:
        pass

    @staticmethod
    def __call__(y_pred: np.ndarray, y_true: np.ndarray) -> float:
        out = np.zeros(y_true.shape)

        return -np.mean(
            np.log(y_pred + epsilon, where=y_true==1, out=out)
            + np.log(1 - y_pred + epsilon, where=y_true==0, out=out)
        )
    
    @staticmethod
    def grad(y_pred: np.ndarray, y_true: np.ndarray) -> np.ndarray:
        return - np.where(y_true == 1, 1 / (y_pred + epsilon), - 1 / (1 - y_pred + epsilon))


if __name__ == '__main__':
    from network import Layer
    # XOR (Goodfelow et al., Deep Learning Book)
    net = NeuralNetwork([
        Layer(2, 2, activation='ReLU', W=np.array([[1, 1], [1, 1]]), b=np.array([0, -1])),
        Layer(2, 1, activation=None, W=np.array([1, -2]).reshape(-1, 1), b=np.zeros(1)),
    ])

    X = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1],
    ])
    y = np.logical_xor(X[:,0], X[:,1]).astype(X.dtype).reshape(-1, 1)

    assert np.isclose(net(X), y).all()

    # simple classification test
    net = NeuralNetwork([
        Layer(2, 2, activation='ReLU'),
        Layer(2, 1, activation='sigmoid'),
    ])

    X = np.vstack([
        np.random.default_rng().normal(0, 1, (20,2)),
        np.random.default_rng().normal(5, 1, (20,2)),
    ])
    y = np.vstack([
        np.zeros((20, 1)),
        np.ones((20, 1)),
    ])

    loss = BCE_Loss()

    net, _ = train(net, X, y, loss, 0.05, 1000)

    y_prob = net(X)
    assert ((y_prob > 0.5) == y).all()