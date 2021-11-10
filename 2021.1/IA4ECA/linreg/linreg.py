import argparse

import matplotlib.pyplot as plt
import numpy as np

def f(x):
    return 2 + 0.8 * x

def get_h(theta):
    def h(x):
        return theta[0] + theta[1] * x

    return h

def J(theta, x, y_true):
    h = get_h(theta)
    y_pred = h(x)

    diff = y_pred - y_true
    J_value = np.mean(diff**2)
    J_grad = np.mean([diff * dx for dx in [1, x]], axis=1)

    return J_value, J_grad

def print_model(theta, x, y_true):
    h = get_h(theta)

    plt.plot(x, f(x), label='f(x)')
    plt.scatter(x, y_true, label='y_true')
    plt.plot(x, h(x), label='h(x)')

    plt.legend()
    plt.grid()

    return plt.gcf()


if __name__ == '__main__':
    #  === CLI SETUP === 
    parser = argparse.ArgumentParser(description='Linear regression exercise.')
    parser.add_argument('epochs', metavar='EPOCHS', type=int, help='number of epochs')
    parser.add_argument('-lr', metavar='learning_rate', dest='lr', type=float,
                        default=0.05, help='learning rate (default: 0.05)')
    parser.add_argument('--print-epochs', dest='plot', action='store_true',
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

    x = np.linspace(-3, 3, 100)
    y_true = f(x) + np.random.randn(*x.shape)

    costs = list()

    theta = np.array([0, 0])
    for e in range(epochs):
        cost, grad = J(theta, x, y_true)
        if cost > 1000:
            break

        epoch_str = f"Epoch {e+1}/{epochs}\nTheta = {theta}\nCost = {cost}\n"
        if plot and (e % 10 == 0):
            print_model(theta, x, y_true)
            plt.suptitle(epoch_str)
            plt.show()
        elif debug:
            print(epoch_str)

        theta = theta - lr * grad

        costs.append(cost)

    print(f"Final model: h(x) = {theta[0]:.2f} + {theta[1]:.2f}x")

    plt.plot(costs, label='MSE')
    plt.grid()
    plt.legend()
    plt.yscale('log')
    plt.suptitle('Loss')
    plt.show()
