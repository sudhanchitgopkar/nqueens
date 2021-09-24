#imOAport statements 
import random
import numpy as np
from deap import creator, base, tools, algorithms

nq = 20

def calcAttacks (indiv):
    attacks = 0 # num total attacks

    # frequency tables
    rowFreq = np.zeros((nq))
    mDiagFreq = np.zeros((2*nq))
    sDiagFreq = np.zeros((2*nq))

    # populates frequency tables
    for i in range(0,nq):
        rowFreq[indiv[i]] += 1
        mDiagFreq[indiv[i] + i] += 1
        sDiagFreq[nq - indiv[i] + i] += 1

    # calculates conflicts based on frequencies
    for i in range(2 * nq):
        if i < nq:
            attacks += (rowFreq[i] * (rowFreq[i] - 1))/2
        attacks += (mDiagFreq[i] * (mDiagFreq[i] - 1))/2
        attacks += (sDiagFreq[i] * (sDiagFreq[i] - 1))/2
        
    return attacks,

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", np.ndarray, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("indices", random.sample,range(nq),nq)
toolbox.register("individual", tools.initIterate,
                 creator.Individual,toolbox.indices)

toolbox.register("population", tools.initRepeat, list,toolbox.individual) 

toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes)
toolbox.register("select", tools.selTournament, tournsize=10)
toolbox.register("evaluate", calcAttacks)

def main():
    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1, similar = np.array_equal)
    CXPB = 0.9
    numEvals = 0
    
    print("Start of evolution")
    
    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
        numEvals += 1
        
    print("  Evaluated %i individuals" % len(pop))
     
    fits = [ind.fitness.values[0] for ind in pop]
    # Variable keeping track of the number of generations
    g = 0

    # Begin the evolution
    while min(fits) > 0 and numEvals < 1000000:
        # A new generation
        g += 1
        print("-- Generation %i --" % g)
        
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                #toolbox.mate(child1, child2,0.5)
                toolbox.mate(child1, child2)
            
                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values
       
        for mutant in offspring:

            # mutate an individual with probability MUTPB
            toolbox.mutate(mutant, 1/nq)
            del mutant.fitness.values
       

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
            numEvals += 1
            
        print("  Evaluated %i individuals" % len(invalid_ind))
        print("  Evaluated %i total individuals" % numEvals)
        
        # The population is entirely replaced by the offspring
        pop[:] = offspring
        
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]
        hof.update(pop)
              
        length = len(pop)
        mean = sum(fits) / length
       # sum2 = sum(x*x for x in fits)
        #std = abs(sum2 / length - mean**2)**0.5
        
        print("  Min %s" % min(fits))
        #print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        #print("  Std %s" % std)
        #print("  Best \n%s" %hof[0])
        
    print (hof[0])
    
main()


