import PopulationUtils
import random as rand
import math
from Specimen import Specimen
import numpy as np


class AbstractAlgorithm(object):
    """
    Defines abstract algorithm structure
    """
    def __init__(self, initialPopulation, fitnessFunction, specimenTemplate, updateCallback):
        self.population = initialPopulation
        self.updateCallback = updateCallback
        self.specimenTemplate = specimenTemplate
        self.fitnessFunction = fitnessFunction
        self.iteration = 0
        self.shouldStop = False

        # Algorithm related variables
        self.bestPopulation = np.array(self.population).copy()

    def reset(self):
        self.iteration = 0

    def setUpdateCallback(self, fn):
        self.updateCallback = fn

    def setSpecimenTemplate(self, template):
        self.specimenTemplate = template

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
    """
    Climbing Hill Algorithm class
    """
    def __init__(self, initialPopulation, fitnessFunction, specimenTemplate, updateCallback):
        AbstractAlgorithm.__init__(self, initialPopulation, fitnessFunction, specimenTemplate, updateCallback)

    def get_widget(self):
        pass

    def step(self):
        # For each specimen in population do one evolution cycle
        for i in range(len(self.population)):
            x = self.population[i]
            # we assume that last parameter is fitness
            N = neighborhood(x[:2], 1, fitness_fn=self.fitnessFunction, specimen_template=self.specimenTemplate)  # or x[:(len(x)-1)]
            best = N[0]
            # Find best specimen in neighbourhood
            for nb in N:
                if nb[2] < best[2]:
                    best = nb
            if best[2] < self.bestPopulation[i][2]:
                self.bestPopulation[i] = best
            self.population[i] = best
        self.iteration += 1

    def run(self, iterations=10):
        # TODO: get iterations from widget
        # iterations = widget.get()
        while self.iteration < iterations:
            self.step()
            self.updateCallback(self.population, self.bestPopulation)
            # Timeout
            # if stop button hit
            if self.shouldStop is True:
                self.shouldStop = False
                break
            self.iteration +=1


def neighborhood(x, d, fitness_fn=None, n=10, specimen_template=None):
    """
    Generates randomly neighbourhood of specimen "x" in given diameter "d"
    :param x: specimen
    :param d: area diameter
    :param fitness_fn: fitness function
    :param specimen_template: template
    :param n: number of neighbours to generate default=10
    :return: list of neighbours
    """
    neighbours = []
    for i in range(n):
        new = []
        for dimension in x:
            # (dimension-d) to always be in parenthesis
            new.append((rand.random() * (dimension+d - (dimension-d))) + (dimension-d))
        if specimen_template is not None:
            PopulationUtils.validate_constrains(new, specimen_template)
        if fitness_fn is not None:
            new.append(fitness_fn(new))
        neighbours.append(new)
    return neighbours


class SimulatedAnnealingAlgorithm(AbstractAlgorithm):
    """
    Simulated Annealing Algorithm class
    """
    def __init__(self, initialPopulation, fitnessFunction, specimenTemplate, updateCallback):
        AbstractAlgorithm.__init__(self, initialPopulation, fitnessFunction, specimenTemplate, updateCallback)
        self.t = 100
        self.alpha = 0.95

    def get_widget(self):
        pass

    def crystallize(self):
        self.t = (self.t * self.alpha)

    def step(self):
        """
        Algorithm itself
        :return:
        """
        n_t = 10
        # For each specimen in population do one evolution cycle
        for i in range(len(self.population)):
            x = self.population[i]
            for j in range(n_t):
                # we assume that last parameter is fitness
                N = neighborhood(x[:2], 1, fitness_fn=self.fitnessFunction, n=1, specimen_template=self.specimenTemplate)  # or x[:(len(x)-1)]

                random_neighbour = N[0]
                delta_f = random_neighbour[2] - x[2]

                if delta_f < 0:
                    # Always accept better solution
                    self.population[i] = random_neighbour
                    # check if best solution changed
                    if self.bestPopulation[i][2] > random_neighbour[2]:
                        self.bestPopulation[i] = random_neighbour
                else:
                    r = rand.random()
                    if r < math.pow(math.e, ((-delta_f)/self.t)):
                        # Accept worse solution
                        self.population[i] = random_neighbour
        # T make lower
        self.crystallize()

    def run(self, t_final=0.1, alpha=0.95):
        self.alpha = alpha
        # TODO: get iterations from widget
        # iterations = widget.get()
        while self.t > t_final:
            self.step()
            self.updateCallback(self.population, self.bestPopulation)
            # Timeout
            # if stop button hit
            if self.shouldStop is True:
                self.shouldStop = False
                break


class DifferentialEvolution(AbstractAlgorithm):
    def __init__(self, initialPopulation, fitnessFunction, specimenTemplate, updateCallback):
        AbstractAlgorithm.__init__(self, initialPopulation, fitnessFunction, specimenTemplate, updateCallback)

        self.F = 0.9
        self.CR = 0.8
        self.generation = 0

    def get_widget(self):
        pass

    def step(self):
        new_population = []
        pop_size = len(self.population)
        for i in range(pop_size):
            actual_specimen = self.population[i]
            # choose 3 random specimen from population
            random_specimens = []
            for j in range(3):
                next_spec_index = rand.randint(0, pop_size-1)
                next_spec = self.population[next_spec_index]
                # if we pick already used, we just increase index until we find unused
                while next_spec in random_specimens:
                    next_spec_index += 1
                    if next_spec_index == pop_size:
                        next_spec_index = 0
                    next_spec = self.population[next_spec_index]

                # now we have unused - use numpy arrays for easy manipulation
                random_specimens.append(np.array(next_spec[:2]))

            # create Differential vector
            differential_vector = np.array(random_specimens[0] - random_specimens[1])
            weighted_differential_vector = self.F * differential_vector
            noise_vector = random_specimens[2] + weighted_differential_vector

            # trial vector - MUTATION part
            trial_vector = []
            for att_index in range(len(noise_vector)):
                probability = rand.random()
                if probability < self.CR:
                    trial_vector.append(noise_vector[att_index])
                else:
                    trial_vector.append(actual_specimen[att_index])

            # constrains
            PopulationUtils.validate_constrains(trial_vector, self.specimenTemplate)
            # count fitness of trial vector
            trial_vector.append(self.fitnessFunction(trial_vector))
            # add to new population one with better fitness
            if trial_vector[2] < actual_specimen[2]:
                new_population.append(trial_vector)
            else:
                new_population.append(actual_specimen)

        # discard old population in favour of new one
        self.population = new_population
        self.generation += 1

    def run(self):
        pass
