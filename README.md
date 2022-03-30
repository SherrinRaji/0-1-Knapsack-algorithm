# 0-1-Knapsack-algorithm
Heuristic and MIP algorithms to solve 0/1 knapsack problem

STEPS for SETUP
1. Create a folder with inputs in the format as in the link below.
http://artemisa.unicauca.edu.co/~johnyortega/instances_01_KP/

2. Add the path to the file in constants.py -> 'FILE_PATH'

You are good to go!

Sample Output:

Population size: (100, 10)
Initial population: 

[[0 1 1 1 0 0 1 0 1 0]
 [1 1 1 1 1 0 1 0 0 0]
 [1 1 0 1 1 0 1 1 0 1]
 [1 1 1 1 0 0 0 0 1 0]
 ..
 [0 1 0 0 1 0 1 1 1 1]]

Final population: 

[[0 1 1 1 0 0 0 1 1 1]
 [0 1 1 1 0 0 0 1 1 1]
 [0 1 1 1 0 0 0 1 1 1]
 [0 1 1 1 0 0 0 1 1 1]
 ..
 [0 1 1 1 0 0 0 1 1 1]]

Fitness of the Final population: 

[295 295 295 295 295 295 295 295 295 295 295 295 295 295 295 295 295 295
 295 295 295 295 295 295 295 295 295 295 295 295 295 295 295 295 295 295
 295 295 295 295 295 295 295 295 295 295 295 295 295 295 295 295 295 295
 295 295 234 295   0 285 295 295 234 295   0   0 285 295 295 285 295 248
 295 210 290 295 295 295 295 295 295 295   0 295 295 295 248 295 295 295
   0 295 295 208 208 290 234   0 295 295]

Maximum value is: 

295 

Items in knapsack: 

[55 10 47  5  4 50  8 61 85 87 55 10 47  5  4 50  8 61 85 87 55 10 47  5
  4 50  8 61 85 87 55 10 47  5  4 50  8 61 85 87 55 10 47  5  4 50  8 61
 85 87 55 10 47  5  4 50  8 61 85 87]
