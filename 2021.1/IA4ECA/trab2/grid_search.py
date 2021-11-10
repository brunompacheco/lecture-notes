from utils import plot_decision_boundaries
import numpy as np
import pandas as pd

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold

from estimator import NeuralNetworkClassifier


if __name__ == '__main__':
    data = np.loadtxt('classification2.txt', delimiter=',')
    X = data[:, :2]
    y = data[:, -1:]

    parameters = {
        'n_hidden': [3, 4, 5, 6],
        'hidden_size': [3, 4, 5, 6, 7],
        'n_epochs': [20000],
        'hidden_activation': ['ReLU'],
        'lr': [0.001, 0.005, 0.01],
    }
    kf = KFold(n_splits=5, shuffle=True, random_state=42)  # fix the split
    clf = GridSearchCV(NeuralNetworkClassifier(), parameters,
                       scoring='accuracy', n_jobs=3, cv=kf.split(X, y))

    clf.fit(X, y)

    cv_results = clf.cv_results_

    best_accu = np.max(cv_results['mean_test_score'])
    best_i = np.argmin(cv_results['rank_test_score'])
    best_params = cv_results['params'][best_i]

    print(f'Best (mean 5-fold) accuracy: {100*best_accu:.2f} %')
    print('Best parameters found:')
    print(best_params)

    # store results
    df = pd.concat([
        pd.DataFrame(clf.cv_results_["params"]),
        pd.DataFrame(clf.cv_results_["mean_test_score"], columns=["Accuracy"]),
    ],axis=1)
    df.to_csv('cv_results.csv')

    net = clf.best_estimator_.net_

    plot_decision_boundaries([net], X, y)
