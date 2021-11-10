#!/usr/bin/env python
__author__ = "Bruno Machado Pacheco"

import argparse
import math

import matplotlib.pyplot as plt
import numpy as np

from random import randint, random, sample

L = 32  # size of chromossome in bits
DOMAIN = (0,math.pi)

# 1.23 -> ’00010111100 ’
def get_bits(x, end=math.pi):
    """Map a float between 0 and `end` into an `L`-sized binary number.

    The transformation is just a scaling between the integer values that fit
    the `L`-sized binary and the desired range. This way, any mutation of the
    binary will remain within the domain of the problem.
    """
    if x > end:
        x = end

    if x < 0:
        x = 0

    int_upper = 2**L - 1

    # float to integer
    scaled_x = (x * int_upper) / end
    int_x = int(scaled_x+0.5)

    # integer to binary
    bin_fmt = '{:0' + str(L) + 'b}'
    bin_x = bin_fmt.format(int_x)

    return bin_x

# ’00010111100 ’ -> 1.23
def get_float(bits, end=math.pi):
    """Inverse of `get_bits`.

    Map any `L`-sized binary value into the 0-`end` interval. 
    """
    assert len(bits) == L

    int_upper = 2**L - 1

    # binary to integer
    int_x = int('0b'+bits, 2)

    # integer to float
    x = (int_x * end) / int_upper

    return x

def f(x):
    """Fitness function.
    """
    if x >= math.pi or x <= 0:
        return 0.0
    else:
        return x + abs(math.sin(32*x))

def mutate(c_bits, p_m):
    """Invert chromosome's bits with probability `p_m`.

    The probability is for the mutation of any given bit, so multiple bits
    mutations are possible.
    """
    new_bits = [str(int(not bool(int(b)))) if random() < p_m else b
                for b in c_bits]
    return ''.join(new_bits)

if __name__ == '__main__':
    #  === CLI SETUP === 
    parser = argparse.ArgumentParser(description='Genetic algorithms exercise.')
    parser.add_argument('n', metavar='N', type=int, help='population size')
    parser.add_argument('g', metavar='G', type=int, help='number of generations')
    parser.add_argument('r', metavar='R', type=int, help='number of runs')
    parser.add_argument('-c', '--crossover', metavar='P_c', dest='p_c',
                        type=float, default=0.5,
                        help='crossover probability (default: 0.5)')
    parser.add_argument('-m', '--mutation', metavar='P_m', dest='p_m',
                        type=float, default=0.001,
                        help='mutation probability (default: 0.001)')
    parser.add_argument('--show-gens', dest='plot', action='store_true',
                        help='Show population plots at each generation.')

    args = parser.parse_args()
    n = args.n
    total_gens = args.g
    total_runs = args.r
    p_c = args.p_c
    p_m = args.p_m
    plot = args.plot
    #  ================= 

    upper = DOMAIN[-1]
    lower = DOMAIN[0]

    # generation plot setup
    x_range = [math.pi*x/1000 for x  in range(0,1000)]
    f_data = [f(x) for x in x_range]

    datas = list()  # data for the final plot
    for r in range(total_runs):
        # generate random initial population
        population = [random()*(upper-lower) + lower for _ in range(n)]

        data = list()  # data for the final plot
        for gen in range(total_gens):
            # calculate fitness for all chromosomes
            fitnesses = [f(c) for c in population]

            # generation plot
            if plot:
                plt.plot(x_range, f_data, label='Fitness function')
                plt.scatter(population, fitnesses, s=5, c='orange', marker='x',
                            label='Chromosomes')
                plt.gca().set_xlim(0,math.pi)
                plt.suptitle(f'Gen. {gen} (Avg = {sum(fitnesses)/n:.2f} / Best = {max(fitnesses):.2f})')
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

            # mutate children
            next_population = [mutate(child, p_m) for child in next_population]

            # gather data
            data.append(fitnesses)

            # setup for next gen
            population = [get_float(child) for child in next_population]
            population = sample(population, k=n)  # in case of odd n

        print(f'Run {r+1}/{total_runs} -- Final avg. fitness = {np.mean(fitnesses):.2f}')
        datas.append(data)

    # final plot setup
    fits = np.array(datas)
    fits = np.mean(fits, axis=-1)
    fits_mean = np.mean(fits, axis=0)
    fits_upper = np.max(fits, axis=0)
    fits_lower = np.min(fits, axis=0)

    # plot line and ranges
    plt.plot(fits_mean, label='average')
    plt.fill_between(list(range(len(fits_mean))), fits_lower, fits_upper,
                     alpha=0.25, label='min-max range')

    # polishing
    plt.suptitle(f'Population of {n} -- {total_runs} runs average -- final fitness = {fits_mean[-1]:.4f}')
    plt.xlim(0,total_gens)
    plt.ylim(2.0,4.2)
    plt.grid()
    plt.legend()
    plt.show()
