import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from utils import *

N_lines = 12  # N_l
N_buses = 12  # N_b
Time = '19:30:00'


if __name__ == '__main__':
    S_times = get_S_times()

    # compute line impedances
    Z = [0.145 + 0.092j, 0.041 + 0.028j, 0.066 + 0.030j, 0.089 + 0.032j,
         0.084 + 0.032j, 0.084 + 0.032j, 0.084 + 0.032j, 0.189 + 0.052j,
         0.164 + 0.053j, 0.074 + 0.031j, 0.074 + 0.031j, 0.064 + 0.033j]
    line_lengths = [2.82, 4.42, 0.61, 0.56, 1.54, 1.12, 2.36, 0.56, 0.89, 0.46,
                    0.44, 1.21]
    Z = [Z_l*line_l for Z_l, line_l in zip(Z, line_lengths)]

    # compute Y
    Y_lines = np.array([1/Z_l for Z_l in Z])

    Y_incidences = [(1,2), (2,3), (3,4), (4,5), (5,6), (5,7), (6,8), (7,8),
                    (8,9), (9,10), (10,11), (11,3)]

    Y_lines = np.eye(len(Y_lines)) * Y_lines

    NI = np.array([
        [ 0, 1,-1, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [ 0, 0, 1,-1, 0, 0, 0, 0, 0, 0, 0, 0,],
        [ 0, 0, 0, 1,-1, 0, 0, 0, 0, 0, 0, 0,],
        [ 0, 0, 0, 0, 1,-1, 0, 0, 0, 0, 0, 0,],
        [ 0, 0, 0, 0, 0, 1,-1, 0, 0, 0, 0, 0,],
        [ 0, 0, 0, 0, 0, 1, 0,-1, 0, 0, 0, 0,],
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        # [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [ 0, 0, 0, 0, 0, 0, 0, 1,-1, 0, 0, 0,],
        [ 0, 0, 0, 0, 0, 0, 0, 0, 1,-1, 0, 0,],
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,-1, 0,],
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,-1,],
        [ 0, 0, 0,-1, 0, 0, 0, 0, 0, 0, 0, 1,],
    ])  # I find it easier to define NI as N_b x N_l (i.e., transposed)
    Y = NI.transpose() @ Y_lines @ NI

    # add shunt impedances to Y_kk
    Y_shunt = [0.008932, 0.000137, 0.001012, 0.001566, 0.000473, 0.000651,
               0.000309, 0.001566, 0.000819, 0.001553, 0.001623, 0.000602]
    Y_shunt = {incidence: Y_s * 1.j for Y_s, incidence in zip(Y_shunt, Y_incidences)}
    for ij, Y_s in Y_shunt.items():
        i, j = ij
        Y[i,i] += Y_s / 2
        Y[j,j] += Y_s / 2

    # define bus power load
    S_res = np.array([
        0.+0.j,
        0.+0.j,
        0.15000+0.03100j,
        0.00276+0.00069j,
        0.00432+0.00108j,
        0.00725+0.00182j,
        0.00550+0.00138j,
        0.+0.j,
        0.00588+0.00147j,
        0.+0.j,
        0.00477+0.00120j,
        0.00331+0.00083j,
    ]) 
    S_ind = np.array([
        0.+0.j,
        0.+0.j,
        0.05000+0.01000j,
        0.00224+0.00139j,
        0.+0.j,
        0.+0.j,
        0.+0.j,
        0.00077+0.00048j,
        0.+0.j,
        0.00574+0.00356j,
        0.00068+0.00042j,
        0.+0.j,
    ])

    # generator power input added
    P_pv_max = 6 / 50  # MW to p.u conversion

    # adjust time-based oscillation
    S = -(S_res * S_times.loc[Time, 'S_res']
          + S_ind * S_times.loc[Time, 'S_ind'])
    S[8] += P_pv_max * S_times.loc[Time, 'P_pv']

    # generate an estimate of the voltage at the busses
    V = np.array([1.+0.j, 1.+0.j] + [0.99 + 0.001j,] * (N_buses - 2))

    # get voltages
    V = gauss_seidel(S, Y, V)

    # show results
    print(f'Results at {Time}')
    print(f'Peak P_pv = {P_pv_max * 50} MW')
    for k in range(N_buses):
        if k > 0:
            V_k = V[k] * 13.8e3
        else:
            V_k = V[k] * 69.0e3

        print(f'Voltage at bus {k} = {print_polar(V_k)} V')

    I_base = np.conj((50.0e6 + 50.0e6j) / (13.8e3 + 0.j))
    for l in range(N_lines):
        V_diff = np.sum(NI[l] * V)

        I_l = V_diff * Y_lines[l,l] * I_base
        print(f"Current at line {l+2} = {print_polar(I_l)} A")
