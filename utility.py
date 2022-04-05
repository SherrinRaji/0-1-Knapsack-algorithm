from knapsack import Item


def to_knapsack_item_list(file_path):
    item_list = []

    with open(file_path, 'r') as file_reader:
        first = file_reader.readline().split()
        length, wmax = int(first[0]), int(first[1])
        for line in file_reader:
            item_list.append(Item(int(line.split()[0]), int(line.split()[1])))
    return item_list, wmax, length
