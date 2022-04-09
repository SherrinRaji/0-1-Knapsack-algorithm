from genetic_algorithm import GeneticAlgorithm
from knapsack import Item,Knapsack
import numpy as np
from constants import *

class GreedyGeneticAlgorithm(GeneticAlgorithm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        super().__dict__.update(kwargs)

    def get_item(self, chromosome):
        item_list_copy = self.item_list
        item_object = dict([(i, Item(chromosome[i]*item_list_copy[i].value, chromosome[i]
                           * item_list_copy[i].weight)) for i in range(self.chromosome_length)])
        return item_object

    def population_correction(self):
        pop_size = (self.population_size, self.chromosome_length)
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

    def solution(self):
        self.initial_population()
        self.population_correction()
        self.fitness_history = np.empty(
            (self.num_of_iterations, self.population.shape[0]))
        for i in range(self.num_of_iterations):
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
    ga = GreedyGeneticAlgorithm(**ga_data)
    ga.solution()
    
if __name__ == "__main__":
    __solution(NUM_OF_GENERATIONS)