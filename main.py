import sys
import numpy as np
import time
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import testFunction as TF



class Form(QtGui.QWidget):
    def __init__(self):
        super(Form, self).__init__()
        # window settings
        self.setWindowTitle("Function Evaluator")

        # Adding main layout
        self.layout = QtGui.QHBoxLayout(self)
        self.setLayout(self.layout)

        # Adding Control Panel layout
        wrapper = QtGui.QWidget()
        self.layout.addWidget(wrapper)
        cpLayout = QtGui.QVBoxLayout()
        wrapper.setLayout(cpLayout)

        mainLabel = QtGui.QLabel("Control panel")
        mainLabel.setAlignment(QtCore.Qt.AlignTop)

        functionSelector = QtGui.QComboBox()
        functionSelector.addItems(['firstDeJong', 'secondDeJong', 'thirdDeJong'])
        functionSelector.connect(functionSelector, QtCore.SIGNAL("currentIndexChanged(int)"), self, QtCore.SLOT("updateUI(int)"))
        btn = QtGui.QPushButton('change', self)

        # Add all widgets into layout
        cpLayout.addWidget(mainLabel)
        cpLayout.addWidget(functionSelector)
        cpLayout.addWidget(btn)



        fig = Figure()
        self.canvas = FigureCanvas(fig)
        self.canvas.setParent(self)
        self.layout.addWidget(self.canvas)
        # create our plot
        self.initializePlot()


    """
    Initialization of MathPlotLib
    - creates canvas, figure etc.
    """
    def initializePlot(self):
        self.axes = self.canvas.figure.add_subplot(111, projection='3d')
        #draw data
        X = np.arange(-3, 3, 0.2)
        #Basic plane
        basicPlane = np.meshgrid(X, X)

        X, Y = basicPlane
        # here choose which test plane use
        Z = TF.firstDeJong(basicPlane)


        surface = Axes3D.plot_surface(self.axes, X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        # self.axes.set_zlim(-1, 1000)
        # in the end just add canvas to layout


    @QtCore.pyqtSlot(int)
    def updateUI(self, index):
        # print self.figure.subplotpars.
        print 'test %s' %(index)
        #draw data
        # X = np.arange(-2, 2, 0.25)
        # #Basic plane
        # basicPlane = np.meshgrid(X, X)
        #
        # X, Y = basicPlane
        #
        # # here choose which test plane use
        # Z = TF.firstDeJong(basicPlane)
        #
        # # self.axes.clear()
        # self.surf.remove()
        # self.surf = Axes3D.plot_surface(self.axes, X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        # self.canvas.draw()



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()