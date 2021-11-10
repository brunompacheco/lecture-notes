import matplotlib.pyplot as plt
import numpy as np

from sklearn.model_selection import train_test_split

from network import NeuralNetwork, Layer
from train import train, BCE_Loss


if __name__ == '__main__':
    data = np.loadtxt('classification2.txt', delimiter=',')
    X = data[:, :2]
    y = data[:, -1:]

    train_data, test_data = train_test_split(data, test_size=0.33)
    X_train = train_data[:, :2]
    y_train = train_data[:, -1:]
    X_test = test_data[:, :2]
    y_test = test_data[:, -1:]

    net = NeuralNetwork([
        Layer(2, 2, activation='ReLU'),
        Layer(2, 1, activation='sigmoid'),
    ])

    loss = BCE_Loss()
    lr = 0.01
    n_epochs = 1000
    net, train_losses, test_losses = train(net, X_train, y_train, loss, lr, n_epochs, X_test, y_test)

    y_pred = net(X_test) > 0.5
    acc = np.sum(y_pred == y_test) / y_test.shape[0]

    plt.plot(train_losses, label='train')
    plt.plot(test_losses, label='test')
    plt.gca().set_xlabel('Epoch')
    plt.gca().set_ylabel('BCE Loss')
    plt.gca().set_title(f'classification1.txt train (final accuracy = {100*acc:.2f}%)')
    plt.show()

    print('Done')
