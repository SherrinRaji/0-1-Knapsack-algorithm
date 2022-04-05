import utility
import numpy as np
import random as rd
from constants import *
import plot_graph

def __solution(num_of_iterations):
    ga = GeneticAlgorithm()
    greedy_ga = GreedyGeneticAlgorith()
    ga_history = ga.solution(num_of_iterations)
    greedy_history = greedy_ga.greedy_solution(num_of_iterations)
    plot_graph.fitness_graph(ga_history,greedy_history)


def get_input():
    return utility.to_knapsack_item_list(FILE_PATH)


class Item:
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight
        if(self.weight == 0):
            self.ratio = 0
        else:
            self.ratio = float(value/weight)


class GeneticAlgorithm:
    def __init__(self):
        self.population = None
        self.fitness = None
        self.item_list, self.max_weight, self.chromosome_length = get_input()
        self.fitness_history = None

    def initial_population(self):
        pop_size = (SOLUTIONS_PER_POP, self.chromosome_length)
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
    def selection(self):
        num_of_parents = int(SOLUTIONS_PER_POP/2)
        parents = np.empty((num_of_parents, self.population.shape[1]))
        for i in range(num_of_parents):
            max_fitness_idx = np.where(self.fitness == np.max(self.fitness))
            parents[i] = self.population[max_fitness_idx[0][0]]
            self.fitness[max_fitness_idx[0][0]] = -99999
        return parents.astype(int)

# One point crossover between two parents in one loop
    def crossover(self, parents):
        num_offspring = SOLUTIONS_PER_POP - parents.shape[0]
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

    def solution(self, num_of_iterations):
        self.initial_population()
        self.fitness_history = np.empty(
            (num_of_iterations, self.population.shape[0]))
        for i in range(num_of_iterations):
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
        pop_size = (SOLUTIONS_PER_POP, self.chromosome_length)

        parents = self.selection()  # elite from the previous population
        offsprings = self.crossover(parents)  # from parent crossover
        # flippin some of the bits in some individuals
        mutants = self.mutation(offsprings)
        population = np.empty(pop_size)
        population[0:parents.shape[0]] = parents
        population[parents.shape[0]:] = mutants
        # some elite individual and other from crossover
        self.population = population.astype(int)


class GreedyGeneticAlgorith(GeneticAlgorithm):
    def __init__(self):
        super().__init__()

    def get_item(self, chromosome):
        item_list_copy = self.item_list
        item_object = dict([(i, Item(chromosome[i]*item_list_copy[i].value, chromosome[i]
                           * item_list_copy[i].weight)) for i in range(self.chromosome_length)])
        return item_object

    def population_correction(self):
        pop_size = (SOLUTIONS_PER_POP, self.chromosome_length)
        greedy_population = np.empty(pop_size)
        ctr = 0
        for e_chromosome in self.population:
            # print("Individual: {} ".format(e_chromosome))
            weight = 0
            greedy_chromosome = np.array(
                [0]*self.population.shape[1]).astype(int)
            item_dict = self.get_item(e_chromosome)
            for item in sorted(item_dict.items(), key=lambda x: x[1].ratio, reverse=True):
                # print("Index: {} v: {}, w: {}, r: {}".format(item[0],item[1].value,item[1].weight, item[1].ratio))
                weight += item[1].weight
                # print("Weight: {}".format(weight))
                if(weight <= self.max_weight):
                    if item[1].weight != 0:
                        greedy_chromosome[item[0]] = 1
                    else:
                        continue
                else:
                    weight -= item[1].weight
                    # print("Weight Exceeded!!")
                    break
            # print(greedy_chromosome)
            greedy_population[ctr] = greedy_chromosome
            ctr += 1
        self.population = greedy_population

    def greedy_solution(self, num_of_iterations):
        self.initial_population()
        self.population_correction()
        self.fitness_history = np.empty(
            (num_of_iterations, self.population.shape[0]))
        for i in range(num_of_iterations):
            self.fitness_history[i] = self.calculate_fitness()
            self.form_new_population()
            self.population_correction()

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
        


if __name__ == "__main__":
    __solution(NUM_OF_GENERATIONS)
