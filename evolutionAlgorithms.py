import PopulationUtils
import random as rand
from Specimen import Specimen
import numpy as np

class AbstractAlgorithm(object):
    """
    Defines abstract algorithm structure
    """
    def __init__(self, initialPopulation, fitnessFunction, updateCallback):
        self.population = initialPopulation
        self.updateCallback = updateCallback
        self.fitnessFunction = fitnessFunction
        self.iteration = 0
        self.shouldStop = False

        # Algorithm related variables
        self.bestPopulation = np.array(self.population).copy()

    def reset(self):
        self.iteration = 0

    def setUpdateCallback(self, fn):
        self.updateCallback = fn

    def setPopulation(self, pop):
        self.reset()
        self.population = pop

    def setFitnessFunction(self, fn):
        self.reset()
        self.fitnessFunction = fn

    def getWidget(self):
        pass

    def step(self):
        pass




class ClimbingHillAlgorithm(AbstractAlgorithm):
    def __init__(self, initialPopulation, fitnessFunction, updateCallback):
        AbstractAlgorithm.__init__(self, initialPopulation, fitnessFunction, updateCallback)

    def get_widget(self):
        pass


    def step(self):
        fn = self.fitnessFunction
        # For each specimen in population do one evolution cycle
        for i in range(len(self.population)):
            x = self.population[i]
            # we assume that last parameter is fitness
            N = neighborhood(x[:2], 1, fitnessFn=self.fitnessFunction) # or x[:(len(x)-1)]
            best = N[0]
            # Find best specimen in neighbourhood
            for nb in N:
                if(nb[2] > best[2]):
                    best = nb
            if best[2] > self.bestPopulation[i][2]:
                self.bestPopulation[i] = best
            self.population[i] = best
        self.iteration += 1

    def run(self, iterations=10):
        # TODO: get iterations from widget
        # iterations = widget.get()
        while(self.iteration < iterations):
            self.step()
            self.updateCallback(self.population, self.bestPopulation)
            # Timeout
            # if stop button hitted
            if self.shouldStop is True:
                self.shouldStop = False
                break
            self.iteration +=1



def neighborhood(x, d, fitnessFn=None, n=10):
    """
    Generates randomly neighbourhood of specimen "x" in given diameter "d"
    :param x: specimen
    :param d: area diameter
    :param n: number of neighbours to generate default=10
    :return: list of neighbours
    """
    neighbours = []
    for i in range(n):
        new = []
        for dimension in x:
            new.append(rand.random() * (dimension+d - dimension-d) + (dimension-d))
        if(fitnessFn is not None):
            new.append(fitnessFn(new))
        neighbours.append(new)
    return neighbours


# def blind_algorithm(iterations, best, best_fitness, specimen_template, f_cost):
#     for i in range(iterations):
#         arg = specimenPopulation.generate_specimen(specimen_template)
#         fitness = f_cost(arg)
#         if fitness < best_fitness:
#             best_fitness = fitness
#             best = arg
#     return best
