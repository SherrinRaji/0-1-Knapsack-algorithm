import numpy as np


class Item:
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight
        if(self.weight == 0):
            self.ratio = 0
        else:
            self.ratio = float(value/weight)


class Knapsack:
    def __init__(self, file_path):
        self.item_list = []
        with open(file_path, 'r') as file_reader:
            first = file_reader.readline().split()
            self.length, self.wmax, self.answer = int(first[0]), int(first[1]), int(first[2])
            for line in file_reader:
                self.item_list.append(
                    Item(int(line.split()[0]), int(line.split()[1])))