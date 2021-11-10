import matplotlib.pyplot as plt
import numpy as np

from network import NeuralNetwork, Layer
from train import BCE_Loss, train_cv
from utils import plot_decision_boundaries, plot_learning_curves


if __name__ == '__main__':
    data = np.loadtxt('classification2.txt', delimiter=',')
    X = data[:, :2]
    y = data[:, -1:]

    net = NeuralNetwork([
        Layer(2, 2, activation='ReLU'),
        Layer(2, 1, activation='sigmoid'),
    ])

    train_losses, test_losses, accus, nets = train_cv(
        net, X, y,
        loss=BCE_Loss(),
        lr=0.01,
        n_epochs=1000,
        k=5,
        reset_weights=True,  # new initial (random) weights for each fold
    )

    plot_learning_curves(train_losses, test_losses, accus)

    plot_decision_boundaries(nets, X, y)

    print('Done')
