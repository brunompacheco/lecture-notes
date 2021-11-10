from copy import copy
from typing import Callable
import numpy as np

from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.estimator_checks import check_estimator
from sklearn.utils import check_array, check_random_state
from sklearn.exceptions import NotFittedError

from network import Layer, NeuralNetwork
from train import BCE_Loss, train


class NeuralNetworkClassifier(BaseEstimator, ClassifierMixin):
    """WARNING: This class was implemented for BINARY classification only

    ...and has lots of rough edges.

    A wrapper of the NeuralNetwork class so I can run GridSearchCV. Implements
    the base minimum for that.
    """
    def __init__(self, n_hidden: int = 0, hidden_size: int = None,
                 hidden_activation: str = 'ReLU',
                 output_activation: str = 'sigmoid', lr: float = 0.01,
                 n_epochs: int = 1000, loss: Callable = BCE_Loss(),
                 random_state: int = 42) -> None:
        super().__init__()

        self.n_hidden = n_hidden
        self.hidden_size = hidden_size

        self.hidden_activation = hidden_activation
        self.output_activation = output_activation

        self.lr = lr
        self.n_epochs = n_epochs
        self.loss = loss

        self.random_state = check_random_state(random_state)

    def set_params(self, **parameters):
        # just so we don't mess up with the random_state 
        if 'random_state' in parameters.keys():
            self.random_state = check_random_state(parameters['random_state'])
            parameters_ = {k:v for k,v in parameters.items() if k != 'random_state'}
        else:
            parameters_ = parameters

        return super().set_params(**parameters_)

    def fit(self, X: np.ndarray, y: np.ndarray):
        X_ = check_array(X)

        y_ = check_array(y, ensure_2d=False)
        if len(y_.shape) == 1:
            y_ = y_.reshape(-1, 1)

        assert X_.shape[0] == y_.shape[0], ValueError('inconsistent # of samples')

        in_size = X_.shape[1]
        out_size = 1  # binary classification only!

        ### build neural network
        if self.hidden_size is not None:
            hidden_size = self.hidden_size
        else:
            hidden_size = out_size

        random_state = copy(self.random_state)

        layers = list()
        layer_input = in_size
        # hidden layers
        for _ in range(self.n_hidden):
            layers.append(Layer(
                input_size=layer_input,
                output_size=hidden_size,
                activation=self.hidden_activation,
                random_state=random_state,
            ))
            layer_input = hidden_size  # to make sure layers fit together

        # output layer
        layers.append(
            Layer(layer_input, out_size, self.output_activation,
                  random_state=random_state)
        )

        self.net_ = NeuralNetwork(layers)

        # train
        self.net_, _ = train(self.net_, X_, y_, self.loss, self.lr,
                             self.n_epochs)

        return self

    def decision_function(self, X: np.ndarray):
        X_ = check_array(X)

        try:
            y_pred = self.net_(X_)
        except AttributeError:
            raise NotFittedError()

        return y_pred.flatten() - 0.5

    def predict(self, X: np.ndarray):
        X_ = check_array(X)

        y_pred = self.decision_function(X_)

        return (y_pred > 0).astype(float)
