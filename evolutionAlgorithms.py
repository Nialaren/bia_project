import PopulationUtils
import random as rand
import math
from Specimen import Specimen
import numpy as np
import itertools


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


class SOMA(AbstractAlgorithm):
    def __init__(self, initialPopulation, fitnessFunction, specimenTemplate, updateCallback):
        AbstractAlgorithm.__init__(self, initialPopulation, fitnessFunction, specimenTemplate, updateCallback)

        self.pathLength = 2  # (1, 5]
        self.stepParam = 1.2  # (0.11, PathLength]
        self.PRT = 0.1  # [0,1]
        self.migration_num = 0
        self.migrations = 10  # [10, user] - same as iterations
        # [+- anything, user ] - optimal around 0.001 if range is 100 - 100.1
        self.minDiv = -1  # minus means, that algorithm terminates after all rounds (migrations)

    def get_widget(self):
        pass

    def generate_perturbation_vector(self, dim):
        perturbation_vector = []
        for i in range(dim):
            if rand.random() < self.PRT:
                perturbation_vector.append(1)
            else:
                perturbation_vector.append(0)
        return perturbation_vector


    def step(self):
        # find leader
        popSize = len(self.population)
        leader_index = 0
        for i in range(popSize):
            if self.population[leader_index][2] > self.population[i][2]:
                leader_index = i
        leader = self.population[leader_index]

        new_population = []
        # Lets migration starts!
        for specimen in self.population:
            if specimen == leader:
                new_population.append(specimen)
                continue

            best_on_path = specimen
            actual_position = specimen
            t = self.stepParam
            # Migration(mutation) of each element
            while t < self.pathLength:
                new_position = []
                dimension = len(specimen[:2])
                pert_vector = self.generate_perturbation_vector(dimension)
                for att_index in range(dimension):
                    if pert_vector[att_index] == 0:
                        new_position.append(actual_position[att_index])
                    else:
                        tmp = actual_position[att_index] + t * (leader[att_index] - actual_position[att_index])
                        new_position.append(tmp)
                # calculate fitness
                new_position.append(self.fitnessFunction(new_position))
                # check if new position is better
                if new_position[2] < best_on_path[2]:
                    best_on_path = new_position
                # increase step
                t += self.stepParam
            new_population.append(best_on_path)
        self.population = new_population
        self.migration_num += 1

class ScatterSearch(AbstractAlgorithm):
    def __init__(self, initialPopulation, fitnessFunction, specimenTemplate, updateCallback):
        AbstractAlgorithm.__init__(self, initialPopulation, fitnessFunction, specimenTemplate, updateCallback)

    def getWidget(self):
        pass

    def step(self):
        size = len(self.population)
        leader_index = 0
        new_population = []



        if len(new_population) == 0:
            new_population = np.array(self.bestPopulation).copy()

        for combination in itertools.product(self.population, new_population):
            print combination[0] + combination[1]


class ParticleSwarm(AbstractAlgorithm):
    def __init__(self, initialPopulation, fitnessFunction, specimenTemplate, updateCallback):
        AbstractAlgorithm.__init__(self, initialPopulation, fitnessFunction, specimenTemplate, updateCallback)

        self.d = len(specimenTemplate) # dimension
        # count v_max - 1/20 of space range
        self.v_max = []
        for att in specimenTemplate:
            d = att[1][1] - (att[1][0])
            self.v_max.append(d/20.0)

        # learning factors [0, 4]
        self.c1 = 1
        self.c2 = 1
        # setrvacnsot - 1 means, its not important argument
        self.w = 1
        self.bestPositions = np.array(initialPopulation).copy()
        # find initial global best position
        self.gBest = self.bestPositions[0]
        for pos in self.bestPositions:
            if self.gBest[self.d] > pos[self.d]:
                self.gBest = pos
        # initialize speed
        self.actualSpeed = [[0]*len(specimenTemplate)] * len(initialPopulation)

    def get_widget(self):
        pass

    def validate_speed_vector(self, to_validate):
        is_correction = False
        for att_i in range(self.d):
            is_negative = to_validate[att_i] < 0
            if abs(to_validate[att_i]) > self.v_max[att_i]:
                is_correction = True
                new_val = rand.random() * self.v_max[att_i]
                if is_negative:
                    new_val = (-new_val)
                to_validate[att_i] = new_val
        # print "Was correction: {0}".format(is_correction)

    def step(self):
        pop_size = len(self.population)
        for i in range(pop_size):
            specimen_pos = self.population[i]
            specimen_best_pos = self.bestPositions[i]
            new_speed = []
            for att_i in range(self.d):
                local_best_tend = self.c1 * rand.random() * (specimen_best_pos[att_i] - (specimen_pos[att_i]))
                global_best_tend = self.c2 * rand.random() * (self.gBest[att_i] - (specimen_pos[att_i]))
                new_speed.append(self.w * self.actualSpeed[i][att_i] + local_best_tend + global_best_tend)

            # speed validation and correction
            self.validate_speed_vector(new_speed)
            self.actualSpeed[i] = new_speed

            # new position update
            new_position = []
            for att_i in range(self.d):
                new_position.append(specimen_pos[att_i] + new_speed[att_i])

            # position validation
            PopulationUtils.validate_constrains(new_position, self.specimenTemplate)

            # count fitness and update new position
            new_position.append(self.fitnessFunction(new_position))
            self.population[i] = new_position

            # control with best local and global
            if self.gBest[self.d] > new_position[self.d]:
                self.gBest = new_position
            if self.bestPositions[i][self.d] > new_position[self.d]:
                self.bestPositions[i] = new_position
        self.iteration += 1


class EvolutionStrategy(AbstractAlgorithm):
    def __init__(self, initialPopulation, fitnessFunction, specimenTemplate, updateCallback):
        AbstractAlgorithm.__init__(self, initialPopulation, fitnessFunction, specimenTemplate, updateCallback)

        self.d = len(specimenTemplate)
        self.types = [(str(n), '<f8') for n in range(self.d)]

        self.sigmas = []
        self.count_variances()

    def count_variances(self):
        n = len(self.population)
        for att in self.specimenTemplate:
            b = att[1][1] - (att[1][0])
            self.sigmas.append(math.sqrt((math.pi*b)/(2*n)))

    def get_widget(self):
        pass

    def step(self):
        pop_size = len(self.population)
        children = []
        for i in range(pop_size):
            new_child = []
            for att_i in range(self.d):
                new_child.append(self.population[i][att_i] + rand.gauss(0, self.sigmas[att_i]))
            # count fitness
            new_child.append(self.fitnessFunction(new_child))
            # add it to children
            children.append(new_child)

        # order them and choose new population
        all_values = np.concatenate([self.population, children])
        sorted_indexes = np.argsort([x[self.d] for x in all_values])
        new_population = []
        for i in range(pop_size):
            new_population.append(all_values[sorted_indexes[i]])
        self.population = new_population
        self.iteration += 1





