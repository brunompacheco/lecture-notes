from typing import List

import matplotlib.pyplot as plt
import numpy as np

from sklearn.utils.extmath import cartesian

from network import NeuralNetwork


def plot_learning_curves(train_losses: np.ndarray, test_losses: np.ndarray, accus: np.ndarray):
    mean_train_losses = train_losses.mean(axis=0)
    # std_train_losses = train_losses.std(axis=0)
    # plt.fill_between(list(range(train_losses.shape[-1])), mean_train_losses - std_train_losses, mean_train_losses + std_train_losses, color='blue', alpha=0.25)
    plt.fill_between(list(range(train_losses.shape[-1])), train_losses.min(axis=0), train_losses.max(axis=0), color='blue', alpha=0.25)
    plt.plot(mean_train_losses, color='blue', label='train')

    mean_test_losses = test_losses.mean(axis=0)
    # std_test_losses = test_losses.std(axis=0)
    # plt.fill_between(list(range(test_losses.shape[-1])), mean_test_losses - std_test_losses, mean_test_losses + std_test_losses, color='orange', alpha=0.25)
    plt.fill_between(list(range(test_losses.shape[-1])), test_losses.min(axis=0), test_losses.max(axis=0), color='orange', alpha=0.25)
    plt.plot(mean_test_losses, color='orange', label='test')

    plt.gca().set_xlabel('Epoch')
    plt.gca().set_ylabel('BCE Loss')
    plt.gca().set_title(f'Learning curve of {train_losses.shape[0]} networks (accuracy = {100*np.mean(accus):.2f} ({100*np.std(accus):.2f})%)')
    plt.legend()
    plt.grid()
    plt.show()

def plot_decision_boundaries(nets: List[NeuralNetwork], X: np.ndarray, y: np.ndarray,
                             x1lim: tuple = (-1.,1.5), x2lim: tuple = (-1.,1.5)):
    """ Plot the decision boundaries of multiple estimators overlapped.
    """
    # decision frontier
    x1s = np.linspace(x1lim[0],x1lim[1],50)
    x2s = np.linspace(x2lim[0],x2lim[1],40)
    xs = cartesian([x1s, x2s])

    for net in nets:
        z = net(xs)
        z = np.array(np.split(z, 50))
        plt.contourf(x1s, x2s, np.squeeze(z).T, [0.,0.5,1.], alpha=1/len(nets))

    X_0 = X[y.flatten() == 0]
    X_1 = X[y.flatten() == 1]
    plt.scatter(X_0[:,0], X_0[:,1], color='blue', label='y == 0')
    plt.scatter(X_1[:,0], X_1[:,1], color='green', label='y == 1')
    plt.gca().set_title(f'Decision boundaries of {len(nets)} networks')
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.colorbar()
    plt.legend()
    plt.show()