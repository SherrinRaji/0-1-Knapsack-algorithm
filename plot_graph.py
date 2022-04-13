from matplotlib import pyplot as plt
import numpy as np
from constants import *
import timeit
from functools import partial
from genetic_algorithm import *
from greedy_genetic_algorithm import *
from modified_genetic_algorithm import *
from time import time


def plot_time(inputs, repeats, n_tests):
    x, y, y_err = [], [], []
    x1, y1, y_err1 = [], [], []
    x2, y2, y_err2 = [], [], []
    for i in inputs:
        knapsack_object = Knapsack(i)
        ga_data = {
            'population_size': 100,
            'population': None,
            'fitness': None,
            'item_list': knapsack_object.item_list,
            'max_weight': knapsack_object.wmax,
            'chromosome_length': knapsack_object.length,
            'fitness_history': None,
            'num_of_iterations': NUM_OF_GENERATIONS
        }
        ga = GeneticAlgorithm(**ga_data)
        greedy_ga = GreedyGeneticAlgorithm(**ga_data)
        parallel_ga = ModifiedGeneticAlgorithm(**ga_data)
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

        timer = timeit.Timer(partial(parallel_ga.solution))
        t = timer.repeat(repeat=repeats, number=n_tests)
        x2.append(greedy_ga.chromosome_length)
        y2.append(np.mean(t))
        y_err2.append(np.std(t) / np.sqrt(len(t)))

    plt.errorbar(x, y, yerr=y_err, fmt='-o', label="Genetic Algorithm")
    plt.errorbar(x1, y1, yerr=y_err1, fmt='-o',
                 label="Greedy Genetic Algorithm")
    plt.errorbar(x2, y2, yerr=y_err2, fmt='-o',
                 label="Parallel Greedy Genetic Algorithm")


def plot_times(inputs, repeats=3, n_tests=1, file_name_prefix=""):
    plot_time(inputs, repeats, n_tests)
    plt.legend()
    plt.xlabel("Input")
    plt.ylabel("Time [s]")
    # plt.xscale('log')
    # plt.yscale('log')
    if not file_name_prefix:
        plt.show()
    else:
        plt.savefig(file_name_prefix + str(round(time() * 1000)))


def fitness_graph(ga_history, greedy_history, modified_history):
    fitness_history_mean = [np.mean(fitness) for fitness in ga_history]
    plt.plot(list(range(NUM_OF_GENERATIONS)),
             fitness_history_mean, label='GA Mean Fitness')
    fitness_history_max = [np.max(fitness) for fitness in ga_history]
    plt.plot(list(range(NUM_OF_GENERATIONS)),
             fitness_history_max, label='GA Max Fitness')
    fitness_history_mean2 = [np.mean(fitness) for fitness in greedy_history]

    plt.plot(list(range(NUM_OF_GENERATIONS)),
             fitness_history_mean2, label='Greedy GA Mean Fitness')

    fitness_history_max2 = [np.max(fitness) for fitness in greedy_history]
    plt.plot(list(range(NUM_OF_GENERATIONS)),
             fitness_history_max2, label='Greedy GA Max Fitness')

    fitness_history_mean3 = [np.mean(fitness) for fitness in modified_history]

    plt.plot(list(range(NUM_OF_GENERATIONS)),
             fitness_history_mean3, label='Parallel Greedy GA Mean Fitness')
    fitness_history_max3 = [np.max(fitness) for fitness in modified_history]

    plt.plot(list(range(NUM_OF_GENERATIONS)),
             fitness_history_max3, label='Parallel Greedy GA Max Fitness')
    plt.legend()
    plt.title('Fitness through the generations')
    plt.xlabel('Generations')
    plt.ylabel('Fitness')
    # plt.show()
    plt.savefig("fitness_graph_" + str(round(time() * 1000)))


def optimality_graph(inputs):
    barWidth = 0.10
    fig = plt.figure()
    br1 = np.arange(len(inputs))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]
    br4 = [x + barWidth for x in br3]
    input_sizes = []
    ga_results = []
    greedy_results = []
    parallel_results = []
    optimal = []

    for i in inputs:
        knapsack_object = Knapsack(i)
        ga_data = {
            'population_size': 100,
            'population': None,
            'fitness': None,
            'item_list': knapsack_object.item_list,
            'max_weight': knapsack_object.wmax,
            'chromosome_length': knapsack_object.length,
            'fitness_history': None,
            'num_of_iterations': NUM_OF_GENERATIONS
        }
        ga = GeneticAlgorithm(**ga_data)
        greedy_ga = GreedyGeneticAlgorithm(**ga_data)
        parallel_ga = ModifiedGeneticAlgorithm(**ga_data)
        ga_sol = int(ga.solution())
        ga_results.append(ga_sol)
        greedy_results.append(int(greedy_ga.solution()))
        parallel_results.append(int(parallel_ga.solution()))
        optimal.append(int(knapsack_object.answer))
        input_sizes.append(int(knapsack_object.length))
    # Make the plot
    plt.bar(br1, ga_results, color='r', width=barWidth,
            edgecolor='grey', label='Genetic Algorithm')
    plt.bar(br2, greedy_results, color='g', width=barWidth,
            edgecolor='grey', label='Greedy Genetic Algorithm')
    plt.bar(br3, parallel_results, color='b', width=barWidth,
            edgecolor='grey', label='Parallel Greedy Genetic Algorithm')
    plt.bar(br4, optimal, color='y', width=barWidth,
            edgecolor='grey', label='Optimal Solution')

    # Adding Xticks
    plt.xlabel('Inputs', fontweight='bold', fontsize=15)
    plt.ylabel('Results', fontweight='bold', fontsize=15)
    plt.xticks([r + barWidth for r in range(len(inputs))], input_sizes)
    plt.legend()
    plt.show()


def __solution(num_of_iterations):
    # To produce the fitness graphs
    knapsack_object = Knapsack(SMALL_FILE_PATH)
    ga_data = {
        'population_size': SOLUTIONS_PER_POP,
        'population': None,
        'fitness': None,
        'item_list': knapsack_object.item_list,
        'max_weight': knapsack_object.wmax,
        'chromosome_length': knapsack_object.length,
        'fitness_history': None,
        'num_of_iterations': num_of_iterations
    }
    ga = GeneticAlgorithm(**ga_data)
    greedy_ga = GreedyGeneticAlgorithm(**ga_data)
    modified_ga = ModifiedGeneticAlgorithm(**ga_data)
    ga.solution()
    greedy_ga.solution()
    modified_ga.solution()
    fitness_graph(ga.fitness_history, greedy_ga.fitness_history,
                  modified_ga.fitness_history)

    # plot graphs to compare running times
    plot_times(FILE_LIST, repeats=1, n_tests=1, file_name_prefix="plot-")

    # bar graphs to compare optimal solutions
    optimality_graph(LARGE_FILE_LIST)


if __name__ == "__main__":
    __solution(NUM_OF_GENERATIONS)
