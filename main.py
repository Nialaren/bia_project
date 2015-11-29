import sys
import numpy as np
import time
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import testFunction as TF
from GUI import Ui_MainWindow
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt, SIGNAL
from functools import partial


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self,parent)
        Ui_MainWindow.__init__(self, parent)
        self.setupUi(self)

        #canvas with graph
        fig = Figure()
        self.graphicsView.canvas = FigureCanvas(fig)
        layout = QVBoxLayout(self.graphicsView)
        self.graphicsView.setLayout(layout)
        layout.addWidget(self.graphicsView.canvas)

        #spinBoxs
        # self.doubleSpinBox.valueChanged.connect(self.updatePlot)
        # self.doubleSpinBox_2.valueChanged.connect(self.updatePlot)

        self.change.clicked.connect(self.updatePlot)
        # self.chooseFunction.connect(self.comboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self, QtCore.SLOT("updatePlot(int)"))
        # self.horizontalSlider.valueChanged("choosingFunction")
        # self.horizontalSlider_2.valueChanged("choosingFunction")
        self.initializePlot()


    """
    Initialization of MathPlotLib
    - creates canvas, figure etc.
    """
    def initializePlot(self):
        self.axes = self.graphicsView.canvas.figure.add_subplot(111, projection='3d')

        #draw data
        X = np.arange(-3, 3, 0.2)
        #Basic plane
        basicPlane = np.meshgrid(X, X)

        X, Y = basicPlane
        # here choose which test plane use
        Z = TF.firstDeJong(basicPlane)


        self.surf = Axes3D.plot_surface(self.axes, X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        # self.axes.set_zlim(-1, 1000)
        # in the end just add canvas to layout

    @QtCore.pyqtSlot(int)
    def updatePlot(self):
        # changed_slider = self.sender()
        # print self.figure.subplotpars./
        # print 'test %s' %(index)
        x1 = self.doubleSpinBox.value()
        x2 = self.doubleSpinBox_2.value()
        x3 = self.doubleSpinBox_3.value()
        function = self.comboBox.currentIndex()

        #draw data
        X = np.arange(x1, x2, x3)

        #Basic plane
        basicPlane = np.meshgrid(X, X)
        X,Y = basicPlane

        functions = [TF.firstDeJong(basicPlane), TF.rosenbrocksSaddle(basicPlane), TF.thirdDeJong(basicPlane), TF.forthDeJong(basicPlane),
                     TF.rastrigin(basicPlane), TF.schewefel(basicPlane), TF.griewangkova(basicPlane), TF.sineEnvelope(basicPlane),
                     TF.sineWave(basicPlane)]
        # here choose which test plane use
        Z = functions[function]

        # self.axes.clear()
        self.surf.remove()
        self.surf = Axes3D.plot_surface(self.axes, X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        self.graphicsView.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Window()

    ui.show()
    sys.exit(app.exec_())