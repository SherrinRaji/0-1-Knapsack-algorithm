from audioop import cross
import utility
import numpy as np
from constants import *
import pandas


def __start():
    GA = GeneticAlgorithm()
    GA.initial_population()
    print(GA.calculate_fitness())
    GA.selection()
    GA.crossover()


def get_input():
    return utility.to_knapsack_item_list('low-dimensional/f1_l-d_kp_10_269')


class Item:
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight


class GeneticAlgorithm:
    def __init__(self):
        self.population = None
        self.fitness = None
        self.item_list, self.max_weight, self.chromosome_length = get_input()
        self.num_generations = 50
        self.parents = None

    def initial_population(self):
        pop_size = (SOLUTIONS_PER_POP, self.chromosome_length)
        print(str.format("Population size: {}", pop_size))
        self.population = np.random.randint(2, size=pop_size)
        print(self.population)

    def calculate_fitness(self):
        self.fitness = np.empty(self.population.shape[0])
        value = [x.value for x in self.item_list]
        weight = [x.weight for x in self.item_list]
        for idx in range(self.population.shape[0]):
            S1 = np.sum(value*self.population[idx])
            S2 = np.sum(weight*self.population[idx])
            if(S2 <= self.max_weight):
                self.fitness[idx] = S1
            else:
                self.fitness[idx] = 0
        return self.fitness.astype(int)

    def selection(self):
        num_of_parents = int(SOLUTIONS_PER_POP/2)
        self.parents = np.empty((num_of_parents, self.population.shape[1]))
        for i in range(num_of_parents):
            max_fitness_idx = np.where(self.fitness == np.max(self.fitness))
            self.parents[i] = self.population[max_fitness_idx[0][0]]
            self.fitness[max_fitness_idx[0][0]] = -99999
        print(self.parents)

    def crossover(self):
        num_offspring = SOLUTIONS_PER_POP - self.parents.shape[0]
        offsprings = np.empty((num_offspring, self.population.shape[1]))
        print("offspring shape: ",offsprings.shape)
        # one-point crossover with bit point 1/2 of total bit size of a chromosome
        ctr = 0
        crossover_point = int(self.chromosome_length/2)
        for i in range(self.parents.shape[0]):
            p1 = i % self.parents.shape[0]
            p2 = (i+1) % self.parents.shape[0]
            offsprings[i:0, crossover_point] = self.parents[p1:0,
                                                              crossover_point]
            offsprings[i:crossover_point,
                       ] = self.parents[p2:crossover_point, ]
            offsprings[i+1:0,
                       crossover_point] = self.parents[p2:0, crossover_point]
            offsprings[i+1:crossover_point,
                       ] = self.parents[p1:crossover_point, ]
            i += 2

        print(offsprings)

if __name__ == "__main__":
    __start()
