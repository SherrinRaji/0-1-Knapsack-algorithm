from matplotlib import pyplot as plt
import numpy as np
from constants import *
import timeit
from functools import partial
from genetic_algorithm import *
from greedy_genetic_algorithm import *
import genetic_algorithm
from time import time

def plot_time(inputs,repeats, n_tests):
    x, y, y_err = [], [], []
    x1, y1, y_err1 = [], [], []
    for i in inputs:
        knapsack_object = Knapsack(i)
        ga_data = {
            'population_size' : knapsack_object.length ** 2,
            'population': None,
            'fitness': None,
            'item_list': knapsack_object.item_list,
            'max_weight' : knapsack_object.wmax,
            'chromosome_length': knapsack_object.length,
            'fitness_history': None,
            'num_of_iterations': NUM_OF_GENERATIONS
        }
        ga = GeneticAlgorithm(**ga_data)
        greedy_ga = GreedyGeneticAlgorithm(**ga_data)
        timer = timeit.Timer(partial(ga.solution))
        t = timer.repeat(repeat=repeats, number=n_tests)
        x.append(ga.chromosome_length)
        y.append(np.mean(t))
        y_err.append(np.std(t) / np.sqrt(len(t)))
        timer = timeit.Timer(partial(greedy_ga.solution))
        t = timer.repeat(repeat=repeats, number=n_tests)
        x1.append(greedy_ga.chromosome_length)
        y1.append(np.mean(t))
        y_err1.append(np.std(t) / np.sqrt(len(t)))
        
    plt.errorbar(x, y, yerr=y_err, fmt='-o', label="Genetic Algorithm")
    plt.errorbar(x1, y1, yerr=y_err1, fmt='-o', label="Greedy Genetuc Algorithm")

# def plot_time(ga, inputs, repeats, n_tests):
#     x, y, y_err = [], [], []
#     for i in inputs:
#         ga.item_list, ga.max_weight, ga.chromosome_length = genetic_algorithm.get_input(i)
#         timer = timeit.Timer(partial(ga.solution))
#         t = timer.repeat(repeat=repeats, number=n_tests)
#         x.append(ga.chromosome_length)
#         y.append(np.mean(t))
#         y_err.append(np.std(t) / np.sqrt(len(t)))
#     plt.errorbar(x, y, yerr=y_err, fmt='-o', label=type(ga))


def plot_times(inputs, repeats=3, n_tests=1, file_name_prefix=""):
    plot_time(inputs, repeats, n_tests)
    plt.legend()
    plt.xlabel("Input")
    plt.ylabel("Time [s]")
    if not file_name_prefix:
        plt.show()
    else:
        plt.savefig(file_name_prefix + str(round(time() * 1000)))

def fitness_max_graph(ga_history,greedy_history):
    fitness_history_max = [np.max(fitness) for fitness in ga_history]
    plt.plot(list(range(NUM_OF_GENERATIONS)),
             fitness_history_max, label='GA Max Fitness')
    fitness_history_max2 = [np.max(fitness) for fitness in greedy_history]
    plt.plot(list(range(NUM_OF_GENERATIONS)),
             fitness_history_max2, label='Greedy GA Max Fitness')
    plt.legend()
    plt.title('Fitness through the generations')
    plt.xlabel('Generations')
    plt.ylabel('Fitness')
    plt.show()
    plt.savefig("fitness_graph_" + str(round(time() * 1000)))


def fitness_mean_graph(ga_history, greedy_history):
    fitness_history_mean = [np.mean(fitness) for fitness in ga_history]
    plt.plot(list(range(NUM_OF_GENERATIONS)),
             fitness_history_mean, label='GA Mean Fitness')
    fitness_history_mean2 = [np.mean(fitness) for fitness in greedy_history]

    plt.plot(list(range(NUM_OF_GENERATIONS)),
             fitness_history_mean2, label='Greedy GA Mean Fitness')
    plt.legend()
    plt.title('Fitness through the generations')
    plt.xlabel('Generations')
    plt.ylabel('Fitness')
    plt.show()
    plt.savefig("fitness_graph_" + str(round(time() * 1000)))


def __solution(num_of_iterations):
    knapsack_object = Knapsack(FILE_PATH)
    ga_data = {
        'population_size' : knapsack_object.length ** 2,
        'population': None,
        'fitness': None,
        'item_list': knapsack_object.item_list,
        'max_weight' : knapsack_object.wmax,
        'chromosome_length': knapsack_object.length,
        'fitness_history': None,
        'num_of_iterations': num_of_iterations
    }
    ga = GeneticAlgorithm(**ga_data)
    greedy_ga = GreedyGeneticAlgorithm(**ga_data)
    ga.solution()
    greedy_ga.solution()
    fitness_max_graph(ga.fitness_history, greedy_ga.fitness_history)
    fitness_mean_graph(ga.fitness_history, greedy_ga.fitness_history)
    # plot_times(FILE_LIST,repeats=1, n_tests=1, file_name_prefix="plot-")
    
if __name__ == "__main__":
    __solution(NUM_OF_GENERATIONS)