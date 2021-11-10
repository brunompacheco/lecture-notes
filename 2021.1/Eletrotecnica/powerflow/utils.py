import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

N_lines = 12  # N_l
N_buses = 12  # N_b

def r2p(c: np.complex, deg=True):
    return np.abs(c), np.angle(c, deg=deg)

def print_polar(c: np.complex):
    m, a = r2p(c)
    return f"{m:.4f}<{a:.4f}º"

def gauss_seidel(S, Y, V=None, debug=False):
    if V is None:
        V = np.array([1. + 0.j,] * N_buses)

    V_diffs = list()
    V_diff = np.inf
    S_diffs = list()
    S_diff = np.inf
    tol = 1e-6
    for e in range(1, 10000+1):
        V_ = V.copy()
        for k in range(2, N_buses):  # first bus is an infinite bus
            if k == 8:
                # Q_pv = np.imag(V_[k] * np.sum([np.conj(Y[j,k]) * np.conj(V_[j]) for j in range(N_buses)]))
                Q_pv = 0
                S_k = S[k] + Q_pv*1.j  # deduce power consumed at bus

                I_jk = [Y[k,j] * V[j] for j in range(N_buses) if j != k]
                I_k = np.conj(S_k) / np.conj(V[k])
                V_[k] = (I_k - np.sum(I_jk)) / Y[k,k]

                # fixed voltage magnitude
                # V_[k] = 1.0 * np.exp(1.j * np.angle(V_[k]))
            else:
                I_jk = [Y[k,j] * V[j] for j in range(N_buses) if j != k]
                I_k = np.conj(S[k])/np.conj(V[k])
                V_[k] = (I_k - np.sum(I_jk)) / Y[k,k]

        # V += (0.00001 / e) * (V_ - V)
        if np.sum(np.abs(V - V_)) < tol:
            break

        V_diff = np.sum(np.abs(V_ - V))
        V_diffs.append(V_diff)
        V = V_.copy()

        I = np.dot(Y,V)
        S_ = V * I
        S_diff = np.sum(np.abs(S_ - S))  # I'm using total error
        S_diffs.append(S_diff)
        if V_diff < tol:
            break

    if debug:
        print(f'Ran for {e} iterations')
        plt.plot(S_diffs, label='S_diffs')
        h1, l1 = plt.gca().get_legend_handles_labels()
        plt.gca().twinx().plot(V_diffs, color='orange', label='V_diffs')
        h2, l2 = plt.gca().get_legend_handles_labels()
        plt.gca().set_title('Convergence of the algorithm')
        plt.legend(h1+h2, l1+l2, loc=5)
        plt.show()

    return V

def get_S_times():
    S_times = pd.read_csv('S.csv')
    S_times = S_times[['Hora.1', 'S_industrial [p.u.]', 'S_residencial [p.u.]']]
    S_times.columns = ['time', 'S_ind', 'S_res']
    S_times['S_ind'] = pd.to_numeric(S_times['S_ind'].str.replace(',','.'))
    S_times['S_res'] = pd.to_numeric(S_times['S_res'].str.replace(',','.'))
    S_times['time'] = pd.to_datetime(S_times['time'])

    pv_times = pd.read_csv('pv.csv', names=['i', 'u1', 'i2', 'P_pv', 'time'])
    pv_times = pv_times[['time', 'P_pv']].iloc[300:]  # discard previous day
    pv_times['P_pv'] = pd.to_numeric(pv_times['P_pv'].str.replace(',','.'))
    pv_times['time'] = pd.to_datetime(pv_times['time'])

    # sync
    S_times['time -1'] = S_times['time'].shift(-1)
    pv_times = pv_times.set_index('time')

    S_times['P_pv'] = S_times.apply(lambda row: pv_times.loc[row['time']:row['time -1'], 'P_pv'].median(), axis=1)
    S_times = S_times.drop('time -1', axis='columns').set_index('time').dropna()

    return S_times
