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

        # Evolution algorithm important properties
        self.testFunctions = None
        self.activeCostFunction = None
        self.actualPopulation = None
        # Plot initialization
        self.initialize_plot()

    """
    Initialization of default plot
    - adds some data to plot.
    """
    def initialize_plot(self):
        self.testFunctions = [TF.firstDeJong, TF.rosenbrocksSaddle, TF.thirdDeJong, TF.forthDeJong,
                     TF.rastrigin, TF.schewefel, TF.griewangkova, TF.sineEnvelope,
                     TF.sineWave]
        self.activeCostFunction = TF.firstDeJong
        # raw data
        x = np.arange(-3, 3, 0.2)

        y = x
        z = self.activeCostFunction(np.meshgrid(x, x))
        self.plotHandler.updatePlot(x, y, z)

    @QtCore.pyqtSlot()
    def update_plot(self):
        x1 = self.mindoubleSpinBox.value()
        x2 = self.maxdoubleSpinBox.value()
        x3 = self.pointsdoubleSpinBox.value()
        self.activeCostFunction = self.testFunctions[self.chooseFunctionComboBox.currentIndex()]
        # raw data
        x = np.arange(x1, x2, x3)

        y = x
        z = self.activeCostFunction(np.meshgrid(x, x))
        self.plotHandler.updatePlot(x, y, z)

    @QtCore.pyqtSlot()
    def generate_population(self):
        n = self.numOfSpecimenSpinBox.value()
        self.actualPopulation = PopulationUtils.generate_population(
                self.getSpecimenTemplate(),
                n,
                self.activeCostFunction)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Window()

    ui.show()
    sys.exit(app.exec_())
