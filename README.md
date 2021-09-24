# N-Queens
## Overview
To solve the N-queens problem using a genetic algorithm, Python was used alongside the evolutionary computation framework DEAP. Below is an overview of the used representation, fitness, crossover, mutation, and termination strategies. Each following subsection discusses the used strategies in greater detail.

| Characteristic | Implementation in GA        |
| -------------- | --------------------------- |
| Representation | Integer vectors of length n |
| Fitness        | Number of conflicting queens|
| Crossover      | Partially matched crossover |
| Mutation       | Index reshuffling           |
| Population     | 300 Individuals             |
| Selection      | Tournament, 10 individuals  |
| Termination    | Fitness 0 or 1,000,000 Evals|
 
where n is the number of queens in the problem.

## Representation
As mentioned in the overview, individuals are represented using a one-dimensional integer array of size n, where n is the number of queens to be placed on the n × n board.

This representation was chosen in lieu of a double array for its efficiency. In the individual array, each cell represents a queen’s location. The index of the array represents the row location of the queen while the contents at that index represent the column location. Because we must necessarily place each queen on a different row to avoid conflicts and no two indices may be the same, this allows for a 1-D array to be used rather than a 2-D array.

Individuals are initialized using a permutation, as this ensures that there will be no column conflicts upon initialization and acts as a sort of smart initialization alongside the use of indices for row location markings. Using ``DEAP``, the following code was written for the initialization of an individual:

```python
creator.create("Individual", np.ndarray, fitness=creator.FitnessMin)
toolbox.register("indices", random.sample,range(nq),nq)
toolbox.register("individual", tools.initIterate,
                 creator.Individual,toolbox.indices)
```