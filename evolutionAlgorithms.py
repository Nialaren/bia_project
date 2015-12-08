import specimenPopulation
import random as rand
import numpy as np


def neighborhood(x, d):
    N = []
    for i in range(10):
        new = []
        for p in x:
            new.append(rand.random() * (p+d - p-d) + (p-d))
        N.append(new)
    return N

def blind_algorithm(iterations, best, best_fitness, specimen_template, f_cost):
    for i in range(iterations):
        arg = specimenPopulation.generate_specimen(specimen_template)
        fitness = f_cost(arg)
        if fitness < best_fitness:
            best_fitness = fitness
            best = arg
    return best

class ClimbingHillAlgorithm(object):
    def __init__(self, pop, costFn, stepCallback):
        self.population = pop
        self.stepCallback = stepCallback
        self.costFunction = costFn
        self.iteration = 0

        # Algorithm related variables
        self.bestX = self.population

    def get_widget(self):
        pass

    def step(self):
        for i in range(len(self.population)):
            neighbours = neighborhood(self.population[i], 1)
            best = neighbours[0]
            for nb in neighbours:
                if(self.costFunction(nb) > self.costFunction(best)):
                    best = nb

            if self.costFunction(best) > self.costFunction(self.bestX[i]):
                self.bestX[i] = best
            self.population[i] = best
        self.iteration += 1
        self.stepCallback(self.population, self.bestX)

    def reset(self):
        self.iteration = 0

    def set_step_callback(self, fn):
        self.stepCallback = fn

    def set_population(self, pop):
        self.reset()
        self.population = pop

    def set_cost_fn(self, fn):
        self.reset()
        self.costFunction = fn
