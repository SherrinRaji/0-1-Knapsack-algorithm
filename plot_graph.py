from matplotlib import pyplot as plt
import numpy as np
from constants import *


def fitness_graph(ga_history, greedy_history):
    fitness_history_mean = [np.mean(fitness) for fitness in ga_history]
    fitness_history_max = [np.max(fitness) for fitness in ga_history]
    plt.plot(list(range(NUM_OF_GENERATIONS)),
             fitness_history_mean, label='GA Mean Fitness')
    plt.plot(list(range(NUM_OF_GENERATIONS)),
             fitness_history_max, label='GA Max Fitness')
    fitness_history_mean2 = [np.mean(fitness) for fitness in greedy_history]
    fitness_history_max2 = [np.max(fitness) for fitness in greedy_history]
    plt.plot(list(range(NUM_OF_GENERATIONS)),
             fitness_history_mean2, label='Greedy GA Mean Fitness')
    plt.plot(list(range(NUM_OF_GENERATIONS)),
             fitness_history_max2, label='Greedy GA Max Fitness')
    plt.legend()
    plt.title('Fitness through the generations')
    plt.xlabel('Generations')
    plt.ylabel('Fitness')
    plt.show()
    # print(np.asarray(fitness_history).shape)
