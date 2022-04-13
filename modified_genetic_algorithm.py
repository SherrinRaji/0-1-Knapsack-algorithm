from constants import *
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
from knapsack import Knapsack
from greedy_genetic_algorithm import GreedyGeneticAlgorithm


class ModifiedGeneticAlgorithm(GreedyGeneticAlgorithm):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        super().__dict__.update(kwargs)
        self.fitness_h = []

    def individual_fitness(self, chromosome):
        values = [x.value for x in self.item_list]
        return np.dot(chromosome, values)

    def selection(self, selection_rate: float = 0.5):
        population = self.population.tolist()
        population.sort(key=lambda p: self.individual_fitness(p), reverse=True)
        return np.array(population[0:int(selection_rate * len(population))])

    def population_rebuild(self):
        self.fitness_h.append(self.calculate_fitness(self.population))
        self.form_new_population()
        self.population_correction()
        return self.population

    def calculate_fitness(self, population):
        self.fitness = np.empty(population.shape[0])
        value = [x.value for x in self.item_list]
        weight = [x.weight for x in self.item_list]
        for idx in range(len(population)):
            S1 = np.sum(value*population[idx])
            S2 = np.sum(weight*population[idx])
            if(S2 <= self.max_weight):
                self.fitness[idx] = S1
            else:
                self.fitness[idx] = 0
        return self.fitness.astype(int)

    def solution(self):
        self.initial_population()
        self.population_correction()
        self.fitness_history = np.empty(
            (self.num_of_iterations, self.population.shape[0]))

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.population_rebuild)
                       for _ in range(int(self.num_of_iterations))]
            population = np.empty((0, self.chromosome_length), dtype=int)
            i = 0
            for f in as_completed(futures):
                self.fitness_history[i] = self.calculate_fitness(f.result())
                i += 1
                population = np.append(population, f.result(), axis=0)
            sorted(self.fitness_history, key=lambda x: np.mean(x))
        print("Length of history in MGA : {}".format(len(self.fitness_history)))

        best_genome = max(population, key=lambda g: self.individual_fitness(g))
        print(best_genome)
        print(self.individual_fitness(best_genome))
        return self.individual_fitness(best_genome)


def __solution(num_of_iterations):
    knapsack_object = Knapsack(FILE_PATH)
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
    ga = ModifiedGeneticAlgorithm(**ga_data)
    ga.solution()


if __name__ == "__main__":
    __solution(NUM_OF_GENERATIONS)
