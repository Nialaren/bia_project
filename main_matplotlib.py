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
        self.setContentsMargins(0,0,0,0)
        #adding layout
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        self.btn = QtGui.QPushButton('change', self)
        # self.btn.clicked.connect(self.updateUI)

        self.layout.addWidget(self.btn)

        # create our plot
        self.initializePlot()


    """
    Initialization of MathPlotLib
    - creates canvas, figure etc.
    """
    def initializePlot(self):
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111, projection='3d')
        #draw data
        X = np.arange(-3, 3, 0.03)
        #Basic plane
        basicPlane = np.meshgrid(X, X)

        X, Y = basicPlane
        # here choose which test plane use
        Z = TF.sineWave(basicPlane)

        print len(X)
        print len(Y)

        surface = Axes3D.plot_surface(self.axes, X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)

        tstart = time.time()
        num_plots = 0
        while time.time()-tstart < 5:
            surface.remove()
            surface = Axes3D.plot_surface(self.axes, X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
            # line.set_ydata(np.random.randn(100)) # set data
            # self.axes.draw_artist(self.axes.patch)
            # self.axes.draw_artist(surface)
            self.canvas.update()
            self.canvas.flush_events()
            num_plots += 1
        print(num_plots/5)




        # self.surf = self.axes.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)


        # self.axes.set_zlim(-1, 1000)
        # in the end just add canvas to layout
        self.canvas.setParent(self)
        self.layout.addWidget(self.canvas)


    def updateUI(self):
        # print self.figure.subplotpars.

        #draw data
        X = np.arange(-2, 2, 0.25)
        #Basic plane
        basicPlane = np.meshgrid(X, X)

        X, Y = basicPlane

        # here choose which test plane use
        Z = TF.firstDeJong(basicPlane)

        # self.axes.clear()
        self.surf.remove()
        self.surf = Axes3D.plot_surface(self.axes, X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        self.canvas.draw()



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()