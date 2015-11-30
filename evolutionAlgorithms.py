import specimenPopulation
import random as rand


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