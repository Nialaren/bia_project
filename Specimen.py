class Specimen(object):
    def __init__(self, parameters):
        self.parameters = parameters
        self.fitness = 0

    def toArray(self):
        return self.parameters + [self.fitness]

    def updateFitness(self, fn):
        self.fitness = fn(self.parameters)