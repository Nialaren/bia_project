import sys
import numpy as np
from PyQt4.QtGui import *
from PyQt4 import QtCore
from GUI import Ui_MainWindow

from PlotHandlers.matplotlibPlotHandler import PlotHandler
# from PlotHandlers.visvisPlotHandler import PlotHandler
# from PlotHandlers.pyqtgraphPlotHandler import PlotHandler
import testFunction as TF
import PopulationUtils
import evolutionAlgorithms as ea

# algorithms - used for switch-like selection
INDEX_ALGORITHM = [None, ea.ClimbingHillAlgorithm, ea.SimulatedAnnealingAlgorithm]

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self,parent)
        Ui_MainWindow.__init__(self, parent)
        self.setupUi(self)

        #canvas with graph
        layout = QVBoxLayout(self.graphicsView)
        layout.setContentsMargins(0,0,0,0)
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
        self.specimenTemplate = None
        self.testFunctions = None
        self.fitness_function = None
        self.actualPopulation = None
        # Plot initialization
        self.initialize_plot()

    def initialize_plot(self):
        """
        Initialize plot
        :return:
        """
        self.testFunctions = [TF.firstDeJong, TF.rosenbrocksSaddle, TF.thirdDeJong, TF.forthDeJong,
                     TF.rastrigin, TF.schewefel, TF.griewangkova, TF.sineEnvelope,
                     TF.sineWave, TF.MultiPurposeFnc]
        self.fitness_function = TF.firstDeJong

        # raw data
        x = np.arange(-3, 3, 0.2)

        y = x
        z = self.fitness_function(np.meshgrid(x, x))
        self.plotHandler.updatePlot(x, y, z)

    @QtCore.pyqtSlot()
    def update_plot(self):
        x1 = self.mindoubleSpinBox.value()
        x2 = self.maxdoubleSpinBox.value()
        x3 = self.pointsdoubleSpinBox.value()
        self.fitness_function = self.testFunctions[self.chooseFunctionComboBox.currentIndex()]
        # raw data
        x = np.arange(x1, x2, x3)

        y = x
        z = self.fitness_function(np.meshgrid(x, x))
        self.plotHandler.updatePlot(x, y, z)

    @QtCore.pyqtSlot()
    def generate_population(self):
        n = self.numOfSpecimenSpinBox.value()
        self.actualPopulation = PopulationUtils.generate_population(
                self.getSpecimenTemplate(),
                n,
                self.fitness_function)
        # Add reference to algorithm
        if self.algorithm is not None:
            self.algorithm.set_population(self.actualPopulation)
        # Show population
        self.plotHandler.updatePopulation(self.actualPopulation)

    def getSpecimenTemplate(self):
        min_const = self.mindoubleSpinBox.value()
        max_const = self.maxdoubleSpinBox.value()
        only_integer = self.intCheckBox.isChecked()

        data_type = 'real'
        if only_integer:
            data_type = 'integer'
        return [(data_type, (min_const, max_const))] * 2

    def updateCallback(self, actualPopulation, bestPopulation):
        self.actualPopulation = actualPopulation
        # TODO: Save best population to log Widget
        self.plotHandler.updatePopulation(self.actualPopulation)

    @QtCore.pyqtSlot()
    def run_button_callback(self):
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
        if index < (len(INDEX_ALGORITHM)-1):
            if INDEX_ALGORITHM[index] is None:
                print 'None'
                return

            self.algorithm = INDEX_ALGORITHM[index](self.actualPopulation, 
                                                    self.fitness_function, 
                                                    self.specimenTemplate, 
                                                    self.updateCallback
                                                    )
            print INDEX_ALGORITHM[index].__name__
        else:
            return
        
        





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Window()

    ui.show()
    sys.exit(app.exec_())
