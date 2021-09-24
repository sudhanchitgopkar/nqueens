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

# Fitness
The fitness function used to evaluate individuals was simply calculating the number of conflicts that occurred on the board. This is to be calculated as follows:

```
Column Conflicts + Diagonal Conflicts
```

Recall that no row conflicts may occur due to the chosen representation. While a na ̈ıve conflict calculation would likely run in O(n2) time, it is possible to use an approach that works in linear (O(n)) time. This function is defined as follows:

```python
def calcAttacks (indiv):
    attacks = 0 # num total attacks
```
To implement this function, three frequency-arrays of length n must be created containing the frequencies of queens in rows, main diagonals, and secondary diagonals. This is implemented below:

```python
# frequency tables
rowFreq = np.zeros((nq))
mDiagFreq = np.zeros((2*nq))
sDiagFreq = np.zeros((2*nq))
# populates frequency tables
for i in range(0,nq):
    rowFreq[indiv[i]] += 1
    mDiagFreq[indiv[i] + i] += 1
    sDiagFreq[nq - indiv[i] + i] += 1
```

Interestingly, it is possible to derive the number of conflicts from the frequency tables generated. This is calculated using the below code:

```python
# calculates conflicts based on frequencies
for i in range(2 * nq):
    if i < nq:
        attacks += (rowFreq[i] * (rowFreq[i] - 1))/2
    attacks += (mDiagFreq[i] * (mDiagFreq[i] - 1))/2
```

In amalgam, this creates a function that allows for the calculation of the used fitness (# conflicts) in linear time. The total number of conflicts can then be simply returned by the function:

```python
         return attacks,
```


