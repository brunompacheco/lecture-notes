import argparse
import math
import struct

import matplotlib.pyplot as plt
import numpy as np

from random import randint, random, choices, sample

L = 4 * 8 # size of chromossome in bits
DOMAIN = (0,math.pi)

# Exemplo : 1.23 -> ’00010111100 ’
def get_bits(x):
    x_bytes = struct.pack('>f', x)  # 4 bytes in a float

    bits = [f"{x_byte:08b}" for x_byte in x_bytes]

    return ''.join(bits)

# Exemplo : ’00010111100 ’ -> 1.23
def get_float(bits):
    # split bytes
    x_bytes = [bits[i:i+8] for i in range(4)]

    # convert from string to num
    x_bytes = [int(x_byte, 2) for x_byte in x_bytes]

    # convert from num to actual bytes
    x_bytes = [x_byte.to_bytes(1, byteorder='big') for x_byte in x_bytes]

    # join the bytes
    x_ = b''.join(x_bytes)

    return struct.unpack('>f', x_)[0]

def f(x):
    """Fitness function.
    """
    if x >= math.pi or x <= 0:
        return 0.0
    else:
        return x + abs(math.sin(32*x))

def mutate(c_bits, p_m):
    """Invert chromosome's bits with probability p_m.
    """
    new_bits = [str(int(not bool(int(b)))) if random() < p_m else b
                for b in c_bits]
    return ''.join(new_bits)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Genetic algorithms exercise.')
    parser.add_argument('n', metavar='N', type=int, help='population size')
    parser.add_argument('g', metavar='G', type=int, help='number of generations')
    parser.add_argument('-c', '--crossover', metavar='P_c', dest='p_c',
                        type=float, default=0.5,
                        help='crossover probability (default: 0.5)')
    parser.add_argument('-m', '--mutation', metavar='P_m', dest='p_m',
                        type=float, default=0.01,
                        help='mutation probability (default: 0.001)')
    parser.add_argument('--show-plots', dest='plot', type=bool, default=False,
                        help='Show population x fitness plots.')

    args = parser.parse_args()
    n = args.n
    total_gens = args.g
    p_c = args.p_c
    p_m = args.p_m
    plot = args.plot

    # generate random population
    upper = DOMAIN[-1]
    lower = DOMAIN[0]

    population = [random()*(upper-lower) + lower for _ in range(n)]

    # curves
    data = {
        'avg_fitness': list(),
        'best_fitness': list(),
        'best_chromossome': list(),
    }
    for gen in range(total_gens):
        # calculate fitness for all chromosomes
        fitnesses = [f(c) for c in population]

        # plot
        if plot:
            x_range = [math.pi*x/1000 for x  in range(0,1000)]
            f_data = [f(x) for x in x_range]
            plt.plot(x_range, f_data, label='Fitness function')
            plt.scatter(population, fitnesses, s=5, c='orange', marker='x', label=f'Gen. {gen} (Avg = {sum(fitnesses)/n:.2f} / Best = {max(fitnesses):.2f})')
            plt.gca().set_xlim(0,math.pi)
            plt.legend()
            plt.show()

        # compute probabilities
        fitnesses = np.nan_to_num(fitnesses)
        total_fitness = sum(fitnesses)
        fitness_p = np.array(fitnesses) / total_fitness

        # get parents and do crossover
        next_population = list()
        while len(next_population) < n:
            dad1, dad2 = np.random.choice(population, 2, replace=False, p=fitness_p)
            dad1_bits = get_bits(dad1)
            dad2_bits = get_bits(dad2)
            if random() <= p_c:
                locus = randint(1,L-1)  # I assume there's always some crossover
                child1 = dad1_bits[:locus] + dad2_bits[locus:]
                child2 = dad2_bits[:locus] + dad1_bits[locus:]
            else:
                child1, child2 = dad1_bits, dad2_bits

            next_population.append(child1)
            next_population.append(child2)

        # mutate childs
        next_population = [mutate(child, p_m) for child in next_population]

        # gather data
        data['avg_fitness'].append(total_fitness / n)
        data['best_fitness'].append(max(fitnesses))
        data['best_chromossome'].append(population[list(fitnesses).index(max(fitnesses))])

        # setup for next gen
        population = [get_float(child) for child in next_population]
        if any([math.isnan(p) for p in population]):
            print('', end='')
        population = sample(population, k=n)  # in case of odd n

    plt.plot(data['avg_fitness'], label='Avg. fitness')
    # plt.plot(data['best_fitness'], label='Best fitness')
    plt.legend()
    plt.show()
    print('Done!')
