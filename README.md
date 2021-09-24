# N-Queens
## Overview
To solve the N-queens problem using a genetic algorithm, Python was used alongside the evolutionary computation framework DEAP. Below is an overview of the used representation, fitness, crossover, mutation, and termination strategies. Each following subsection discusses the used strategies in greater detail.

| Representation | Integer vectors of length n |
| -------------- | --------------------------- |
| Fitness        | Number of conflicting queens|

| Crossover      | Partially matched crossover |

| Mutation       | Index reshuffling           |

| Population     | 300 Individuals             |

| Selection      | Tournament, 10 individuals  |

| Termination    | Fitness 0 or 1,000,000 Evals|
 