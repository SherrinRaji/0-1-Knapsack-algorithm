from audioop import cross
import re
import utility
import numpy as np
import random as rd
from constants import *
import pandas


def __solution(num_of_iterations):
    ga = GeneticAlgorithm()
    ga.initial_population()
    fitness_history = np.empty((num_of_iterations, ga.population.shape[0]))
    for i in range(num_of_iterations):
        fitness_history[i] = ga.calculate_fitness()
        ga.population = __form_new_population(ga)
    
    print("Final population: \n{}".format(ga.population))
    #calculate fitness of last gen
    last_population_fitness = ga.calculate_fitness()
    print("Fitness of the Final population: \n{}".format(last_population_fitness))
    
    #The set of items that give the optimal result
    

def __form_new_population(ga):
    pop_size = (SOLUTIONS_PER_POP, ga.chromosome_length)

    parents = ga.selection()
    offsprings = ga.crossover(parents)
    mutants = ga.mutation(offsprings)
    population = np.empty(pop_size)
    population[0:parents.shape[0]] = parents
    population[parents.shape[0]:] = mutants
    return population


def get_input():
    return utility.to_knapsack_item_list('low-dimensional/f6_l-d_kp_10_60')


class Item:
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight


class GeneticAlgorithm:
    def __init__(self):
        self.population = None
        self.fitness = None
        self.item_list, self.max_weight, self.chromosome_length = get_input()

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

# Getting the top four from population as parents for a crossover.
    def selection(self):
        num_of_parents = int(SOLUTIONS_PER_POP/2)
        parents = np.empty((num_of_parents, self.population.shape[1]))
        for i in range(num_of_parents):
            max_fitness_idx = np.where(self.fitness == np.max(self.fitness))
            parents[i] = self.population[max_fitness_idx[0][0]]
            self.fitness[max_fitness_idx[0][0]] = -99999
        return parents

# One point crossover between two parents in one loop
    def crossover(self, parents):
        num_offspring = SOLUTIONS_PER_POP - parents.shape[0]
        offsprings = np.empty((num_offspring, self.population.shape[1]))

        # one-point crossover with bit point 1/2 of total bit size of a chromosome
        crossover_point = int(self.chromosome_length/2)
        for i in range(0, parents.shape[0], 2):
            p1 = i % parents.shape[0]
            p2 = (i+1) % parents.shape[0]

            offsprings[i, 0:crossover_point] = parents[p1,
                                                       0:crossover_point]
            offsprings[i, crossover_point:,
                       ] = parents[p2, crossover_point:]
            offsprings[i+1,
                       0:crossover_point] = parents[p2, 0: crossover_point]
            offsprings[i+1, crossover_point:
                       ] = parents[p1, crossover_point:]
        return offsprings

    def mutation(self, offsprings):
        mutants = np.empty((offsprings.shape))
        mutation_rate = 0.4
        for i in range(mutants.shape[0]):
            random_value = rd.random()
            mutants[i, :] = offsprings[i, :]
            if random_value > mutation_rate:
                continue
            int_random_value = rd.randint(0, offsprings.shape[1]-1)
            if mutants[i, int_random_value] == 0:
                mutants[i, int_random_value] = 1
            else:
                mutants[i, int_random_value] = 0

        return mutants


if __name__ == "__main__":
    __solution(100)
