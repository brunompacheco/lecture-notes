from typing import Callable, List

import numpy as np

from scipy.special import expit
from sklearn.utils import check_random_state


class Layer():
    """ A simple layer of a neural network.

    All activations are the same.
    """
    def __init__(self, input_size: int, output_size: int,
                 activation: str = None, W: np.ndarray = None,
                 b: np.ndarray = None, random_state=None) -> None:
        # define activation function together with its gradient
        if activation == 'ReLU':
            def f(x):
                return x * (x > 0)
            def f_grad(x):
                return (x > 0).astype(np.float)
        elif activation == 'sigmoid':
            f = expit
            def f_grad(x):
                return expit(x) * (1 - expit(x))
        elif activation == 'tanh':
            f = np.tanh
            def f_grad(x):
                return 1. - np.tanh(x)**2
        else:
            def f(x):
                return x
            def f_grad(x):
                return np.ones(x.shape)

        self._f = f
        self._f_grad = f_grad 

        self.input_size = input_size
        self.output_size = output_size
        self.activation = activation

        if random_state is None:
            self.random_state = np.random
        else:
            self.random_state = check_random_state(random_state)

        self.reset_weights(W, b)

    def reset_weights(self, W: np.ndarray = None, b: np.ndarray = None):
        """ Generate "random" weights given distributions suited for the activation.
        """
        M = self.input_size
        N = self.output_size

        if W is not None:
            self._W = W.copy()
        else:
            if self.activation in ['sigmoid', 'tanh']:
                # normalized Xavier weights
                lower = -6.0 / np.sqrt(M + N)
                upper = 6.0 / np.sqrt(M + N)
                self._W = lower + (upper - lower) * self.random_state.rand(M, N)
            elif self.activation == 'ReLU':
                # Kaiming He weights
                self._W = self.random_state.normal(
                    0,
                    np.sqrt(2 / M),
                    (M, N)
                )
            else:
                self._W = self.random_state.rand(M, N) - 0.5

        if b is not None:
            self._b = b.copy()
        else:
            self._b = np.ones((1, N)) * 0.1

    def __call__(self, X: np.ndarray) -> np.ndarray:
        h = X @ self._W + self._b
        return self._f(h)

    def grad(self, X: np.ndarray) -> np.ndarray:
        """ The gradient of the activation function at the activation of the input
        """
        h = X @ self._W + self._b
        return self._f_grad(h)

    def update_weights_return_input_error(self, X: np.ndarray, error: np.ndarray,
                                          lr: float) -> np.ndarray:
        """ Basically one step of the gradient descent for this layer.
        """
        grad = self.grad(X) * error
        error_next = grad @ self._W.transpose()

        self._W -= lr * (X.transpose() @ grad) / X.shape[0]
        self._b -= lr * np.mean(grad, axis=0).reshape(1, -1)

        return error_next

class NeuralNetwork():
    """ Pack of methods to train and call a stack of layers (aka network).
    """
    def __init__(self, layers: List[Layer]) -> None:
        self.layers = layers

    def __call__(self, x: np.ndarray) -> np.ndarray:
        x_ = x.copy()

        for layer in self.layers:
            x_ = layer(x_)

        return x_

    def descent_step(self, X: np.ndarray, lr: float, loss: Callable,
                     y_true: np.ndarray) -> None:
        """ Run one step of the gradient descent on ALL weights.

        No dropout, no stochastic gd (unless you do it yourself).
        """
        # forward pass
        X_l = [X.copy()]
        for layer in self.layers:
            X_l.append(layer(X_l[-1]))

        y_pred = X_l[-1]
        X_l = X_l[:-1]

        # backward pass
        error = loss.grad(y_pred, y_true)
        for layer, X_ in zip(self.layers[::-1], X_l[::-1]):
            error = layer.update_weights_return_input_error(X_, error, lr)

    def reset_weights(self) -> None:
        """ See Layer.reset_weights().
        """
        for l in self.layers:
            l.reset_weights()
