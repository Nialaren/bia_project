import sys
import numpy as np
from PyQt4.QtGui import *
from PyQt4 import QtCore
from GUI import Ui_MainWindow

from PlotHandlers.matplotlibPlotHandler import PlotHandler
# from PlotHandlers.visvisPlotHandler import PlotHandler
# from PlotHandlers.pyqtgraphPlotHandler import PlotHandler
import testFunction as tF
import PopulationUtils
import evolutionAlgorithms as eA

# algorithms - used for switch-like selection
INDEX_ALGORITHM = [
    None,
    eA.ClimbingHillAlgorithm,
    eA.SimulatedAnnealingAlgorithm,
    eA.DifferentialEvolution,
    eA.SOMA
]


class AppWindow(QMainWindow, Ui_MainWindow):
    """
    Root application widget
    """
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # canvas with graph
        layout = QVBoxLayout(self.graphicsView)
        layout.setContentsMargins(0, 0, 0, 0)
        self.graphicsView.setLayout(layout)
        # create plotHandler
        self.plotHandler = PlotHandler(self)
        layout.addWidget(self.plotHandler.get_widget())

        self.changeButton.clicked.connect(self.update_plot)
        self.generateButton.clicked.connect(self.generate_population)

        # ToolBox with algorithms
        QtCore.QObject.connect(self.chooseSearchToolBox,
                               QtCore.SIGNAL('currentChanged(int)'),
                               self,
                               QtCore.SLOT('algorithm_change_callback(int)')
                               )

        # Run button
        self.ButtonRun.clicked.connect(self.run_button_callback)
        # Step Button
        self.ButtonStep.clicked.connect(self.step_button_callback)

        # Evolution algorithm important properties
        self.algorithm = None
        self.test_functions = None
        self.fitness_function = None
        self.actualPopulation = None
        # Plot initialization
        self.initialize_plot()

    def initialize_plot(self):
        """
        Initialize plot and test functions
        :return:
        """
        self.test_functions = [
            tF.firstDeJong, tF.rosenbrocksSaddle, tF.thirdDeJong, tF.forthDeJong,
            tF.rastrigin, tF.schewefel, tF.griewangkova,
            tF.sineEnvelope, tF.sineWave, tF.MultiPurposeFnc
        ]
        self.update_plot()

    @QtCore.pyqtSlot()
    def update_plot(self):
        """
        Updates fitness function surface graph
        If there is some population - generates new one
        """
        x1 = self.mindoubleSpinBox.value()
        x2 = self.maxdoubleSpinBox.value()
        x3 = self.pointsdoubleSpinBox.value()
        self.fitness_function = self.test_functions[self.chooseFunctionComboBox.currentIndex()]

        # regenerate population
        if self.actualPopulation is not None:
            template = self.get_specimen_template()
            n = self.numOfSpecimenSpinBox.value()
            # generate new population
            self.actualPopulation = PopulationUtils.generate_population(
                    self.get_specimen_template(),
                    n,
                    self.fitness_function
            )

            # Add reference to algorithm and update
            if self.algorithm is not None:
                self.algorithm.set_specimen_template(template)
                self.algorithm.set_population(self.actualPopulation)

        # surface plot data
        x = np.arange(x1, x2, x3)

        y = x
        z = None
        if self.fitness_function.__name__ is tF.MultiPurposeFnc.__name__:
            print 'gooo'
            z = tF.MultiPurposeFnc.graph_z(x, y)
        else:
            z = self.fitness_function(np.meshgrid(x, x))
        # Draw all at once
        self.plotHandler.updatePlot(x, y, z, population=self.actualPopulation)



    @QtCore.pyqtSlot()
    def generate_population(self):
        """
        Generate Population and set it
        :return:
        """
        template = self.get_specimen_template()
        n = self.numOfSpecimenSpinBox.value()
        self.actualPopulation = PopulationUtils.generate_population(
                template,
                n,
                self.fitness_function)
        # Add reference to algorithm
        if self.algorithm is not None:
            self.algorithm.set_specimen_template(template)
            self.algorithm.set_population(self.actualPopulation)
        # Show population
        self.plotHandler.updatePopulation(self.actualPopulation)

    def get_specimen_template(self):
        """
        Generates specimen template according to given constraints
        :return:
        """
        min_const = self.mindoubleSpinBox.value()
        max_const = self.maxdoubleSpinBox.value()
        only_integer = self.intCheckBox.isChecked()

        data_type = 'real'
        if only_integer:
            data_type = 'integer'
        return [(data_type, (min_const, max_const))] * 2

    def update_callback(self, actual_population, best_population, done=False):
        """
        Callback for algorithms to trigger after each iteration
        :param actual_population:
        :param best_population:
        :param done:
        :return:
        """
        self.actualPopulation = actual_population
        # TODO: Save best population to log Widget
        if done:
            print 'Algorithm finished'
            # self.actualPopulation = best_population
            self.plotHandler.updatePopulation(best_population)
        else:
            self.plotHandler.updatePopulation(self.actualPopulation)

    @QtCore.pyqtSlot()
    def run_button_callback(self):
        """
        Execute algorithm
        :return:
        """
        if self.algorithm is not None:
            self.algorithm.run()

    @QtCore.pyqtSlot()
    def step_button_callback(self):
        """
        Triggers when step button is clicked
        :return:
        """
        if self.algorithm is not None:
            self.algorithm.step()
            self.plotHandler.updatePopulation(self.algorithm.population)

    @QtCore.pyqtSlot(int)
    def algorithm_change_callback(self, index):
        """
        Triggers when algorithm is changed from toolbox
        :param index:
        :return:
        """
        if index < (len(INDEX_ALGORITHM)):
            if INDEX_ALGORITHM[index] is None:
                print 'None'
                return

            self.algorithm = INDEX_ALGORITHM[index](self.actualPopulation, 
                                                    self.fitness_function, 
                                                    self.get_specimen_template(),
                                                    self.update_callback
                                                    )
            print '{0} - {1} selected '.format(index, INDEX_ALGORITHM[index].__name__)
        else:
            return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = AppWindow()

    ui.show()
    sys.exit(app.exec_())
