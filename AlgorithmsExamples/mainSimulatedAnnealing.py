import sys
import numpy as np
import time
from PyQt4.QtGui import *
from PyQt4 import QtCore

from PlotHandlers.matplotlibPlotHandler import PlotHandler
import testFunction as TF
import PopulationUtils
import evolutionAlgorithms as EA


class Window(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setWindowTitle('Simulated Annealing')

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

        # create plotHandler
        self.plotHandler = PlotHandler(self)
        layout.addWidget(self.plotHandler.get_widget())

        # create step Button
        self.stepButton = QPushButton(self)
        self.stepButton.setText('Step')

        layout.addWidget(self.stepButton)

        self.stepButton.clicked.connect(self.step)

        self.runButton = QPushButton(self)
        self.runButton.setText('Run')

        layout.addWidget(self.runButton)
        self.runButton.clicked.connect(self.run)

        # Evolution algorithm important properties
        self.algorithm = None
        self.specimenTemplate = None
        self.testFunctions = None
        self.fitnessFunction = None
        self.actualPopulation = None
        self.bestPopulation = None
        self.iteration = 0
        # Plot initialization
        self.initialize_plot()

    @QtCore.pyqtSlot()
    def step(self):
        if self.algorithm is None:
            self.algorithm = EA.SimulatedAnnealingAlgorithm(
                self.actualPopulation,
                self.fitnessFunction,
                self.specimenTemplate,
                self.updateCallback)  # Not needed here
        # Its interesting that self.actualPopulation is given to algorithm via reference
        # So all changes inside algorithm are also shown here
        self.plotHandler.updatePopulation(self.actualPopulation)
        self.algorithm.step()
        # self.algorithm.t +=1
        print 'Actual temperature {0}'.format(self.algorithm.t)

    @QtCore.pyqtSlot()
    def run(self):
        if self.algorithm is None:
            self.algorithm = EA.SimulatedAnnealingAlgorithm(
                self.actualPopulation,
                self.fitnessFunction,
                self.specimenTemplate,
                self.updateCallback)
        self.algorithm.run()

    def initialize_plot(self):
        """
         Initialization of default plot
        - adds some data to plot.
        :return:
        """
        self.fitnessFunction = TF.firstDeJong
        # raw data
        x = np.arange(-3, 3, 0.2)

        y = x
        z = self.fitnessFunction(np.meshgrid(x, x))
        self.plotHandler.updatePlot(x, y, z)
        self.generate_population(10)

    @QtCore.pyqtSlot()
    def generate_population(self, n):
        """
        Generates population with size of N
        :param n:
        :return:
        """
        self.specimenTemplate = self.getSpecimenTemplate(-3, 3)
        self.actualPopulation = PopulationUtils.generate_population(
                self.specimenTemplate,
                n,
                self.fitnessFunction)
        # Show population
        self.plotHandler.updatePopulation(self.actualPopulation)

    def getSpecimenTemplate(self, min_const, max_const, only_integer=False):
        """
        Returns specimen template
        :param min_const:
        :param max_const:
        :param only_integer:
        :return:
        """
        data_type = 'real'
        if only_integer:
            data_type = 'integer'
        return [(data_type, (min_const, max_const))] * 2

    def updateCallback(self, actual_population, best_population):
        """
        Update callback
        :param actual_population:
        :param best_population:
        :return:
        """
        # print 'NEW'
        # print actual_population
        self.bestPopulation = best_population
        # self.actualPopulation = actual_population
        self.plotHandler.updatePopulation(self.actualPopulation)
        print 'Iteration {0}'.format(self.iteration)
        self.iteration += 1
        # time.sleep(2)
        # self.algorithm.shouldStop = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Window()

    ui.show()
    sys.exit(app.exec_())