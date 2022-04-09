import numpy as np
import random as rd
from constants import *
from knapsack import Knapsack

class GeneticAlgorithm:
    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)
        

    def initial_population(self):
        pop_size = (self.population_size, self.chromosome_length)
        print(str.format("Population size: {}", pop_size))
        self.population = np.random.randint(2, size=pop_size)
        
        print("Initial population: \n\n{}".format(self.population.astype(int)))

    def get_knapsack_items(self, chromosome):
        items = np.empty(self.population.shape[1])
        for i in range(self.population.shape[1]):
            items[i] = chromosome[i]*self.item_list[i].value
        return items.astype(int)

    def calculate_fitness(self):
        # print("this works! {}".format(self.population.shape[0]))
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
    def selection(self,selection_rate:float=0.5):
        num_of_parents = int(self.population_size*selection_rate)
        parents = np.empty((num_of_parents, self.population.shape[1]))
        for i in range(num_of_parents):
            max_fitness_idx = np.where(self.fitness == np.max(self.fitness))
            parents[i] = self.population[max_fitness_idx[0][0]]
            self.fitness[max_fitness_idx[0][0]] = -99999
        return parents.astype(int)

# One point crossover between two parents in one loop
    def crossover(self, parents):
        num_offspring = self.population_size - parents.shape[0]
        offsprings = np.empty((num_offspring, self.population.shape[1]))

        # one-point crossover with bit point 1/2 of total bit size of a chromosome
        crossover_point = int(self.chromosome_length/2)
        for i in range(0, parents.shape[0], 2):
            if(i+1 < parents.shape[0]):
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
        return offsprings.astype(int)

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

        return mutants.astype(int)

    def solution(self):
        self.initial_population()
        self.fitness_history = np.empty(
            (self.num_of_iterations, self.population.shape[0]))
        for i in range(self.num_of_iterations):
            self.fitness_history[i] = self.calculate_fitness()
            self.form_new_population()

        print("\nFinal population: \n\n{}".format(self.population))
        # calculate fitness of last gen
        last_population_fitness = self.calculate_fitness()
        print("\nFitness of the Final population: \n\n{}".format(
            last_population_fitness))

        # The set of items that give the optimal result
        max_fitness_pos = np.where(
            last_population_fitness == np.max(last_population_fitness))
        items = self.get_knapsack_items(self.population[max_fitness_pos[0][0]])
        print("\nMaximum value is: \n\n{} \n Items in knapsack: \n\n{}".format(
            last_population_fitness[max_fitness_pos[0][0]], items.astype(int)))

    def form_new_population(self):
        pop_size = (self.population_size, self.chromosome_length)

        parents = self.selection()  # elite from the previous population
        offsprings = self.crossover(parents)  # from parent crossover
        # flippin some of the bits in some individuals
        mutants = self.mutation(offsprings)
        population = np.empty(pop_size)
        population[0:parents.shape[0]] = parents
        population[parents.shape[0]:] = mutants
        # some elite individual and other from crossover
        self.population = population.astype(int)


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
    ga.solution()
    
if __name__ == "__main__":
    __solution(NUM_OF_GENERATIONS)