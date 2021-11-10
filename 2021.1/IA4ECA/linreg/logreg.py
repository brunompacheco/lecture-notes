import argparse

import matplotlib.pyplot as plt
import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def get_h(theta):
    def h(x):
        return sigmoid(theta[0] + theta[1] * x)

    return h

def J(theta, x, y_true):
    h = get_h(theta)
    y_pred = h(x)

    J_value = -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
    J_grad = np.mean([(y_pred - y_true) * x_i for x_i in [1, x]], axis=1)

    return J_value, J_grad

def plot_model(theta, x, y_true):
    h = get_h(theta)

    x0 = x[y_true == 0]
    x1 = x[y_true == 1]
    plt.scatter(x0, np.ones(x0.shape), label='0')
    plt.scatter(x1, np.zeros(x1.shape), label='1')
    if theta[1] != 0:
        x_frontier = - theta[0] / theta[1]
        plt.vlines(x_frontier, 0, 1, label='frontier')

    plt.legend()
    plt.grid()

    return plt.gcf()

def accuracy(y_true, y_pred):
    y_pred_ = y_pred > 0.5
    y_true_ = y_true > 0.5

    return np.mean(y_true_ == y_pred_)


if __name__ == '__main__':
    #  === CLI SETUP === 
    parser = argparse.ArgumentParser(description='Logistic regression exercise.')
    parser.add_argument('epochs', metavar='EPOCHS', type=int, help='number of epochs')
    parser.add_argument('-lr', metavar='learning_rate', dest='lr', type=float,
                        default=0.05, help='learning rate (default: 0.05)')
    parser.add_argument('--plot-epochs', dest='plot', action='store_true',
                        help='plot models every 10 epochs.')
    parser.add_argument('--debug', dest='debug', action='store_true',
                        help='print epoch results.')

    args = parser.parse_args()
    epochs = args.epochs
    lr = args.lr
    plot = args.plot
    debug = args.debug
    #  ================= 
    np.random.seed(42)

    # data setup
    mean0, std0 = -0.4, 0.5
    mean1, std1 = 0.9, 0.3
    m = 200
    x = np.hstack((
        np.random.randn(m//2) * std0 + mean0,
        np.random.randn(m//2) * std1 + mean1,
    ))
    y_true = np.hstack((np.ones(m//2), np.zeros(m//2)))

    # initial parameters
    theta = np.array([0.001, 0.001])

    costs = list()
    accs = list()
    for e in range(epochs):
        cost, grad = J(theta, x, y_true)
        if cost > 1000:
            break

        acc = accuracy(y_true, get_h(theta)(x))
        epoch_str = f"Epoch {e+1}/{epochs}\nTheta = {theta}\nCost = {cost}\nAccuracy = {acc}\n"
        if plot and (e % 10 == 0):
            plot_model(theta, x, y_true)
            plt.suptitle(epoch_str)
            plt.show()
        elif debug:
            print(epoch_str)

        theta = theta - lr * grad

        costs.append(cost)
        accs.append(acc)

    print(f"Final model: h(x) = sig({theta[0]:.2f} + {theta[1]:.2f}x)")
    print(f"Accuracy = {acc}")
    print(f"Separation at x = {-theta[0]/theta[1]}")

    plt.plot(costs, label='BCE')
    plt.xlabel('epoch')
    plt.gca().twinx().plot(accs, color='orange', label='Accuracy')
    plt.grid()
    plt.legend()
    plt.suptitle('Loss')
    plt.show()
