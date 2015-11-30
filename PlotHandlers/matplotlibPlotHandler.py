from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

class PlotHandler(object):
    def __init__(self, parent):
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111, projection='3d')
        self.canvas.setParent(parent)
        self.activePlot = None
        self.activePopulation = None

        self.surface = None
        self.scatter = None

    def get_widget(self):
        return self.canvas

    def updatePlot(self, X, Y, Z):
        self.activePlot = (X,Y,Z)

        if self.surface is not None:
            self.surface.remove()

        self.surface = Axes3D.plot_surface(self.axes, X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        self.canvas.draw()

    def updatePopulation(self, population):
        # X,Y,Z = self.activePlot
        #
        # if self.surface is not None:
        #     self.surface.remove()
        #
        # self.surface = Axes3D.plot_surface(self.axes, X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)


        self.activePopulation = population
        x, y, z = self.prepare_population_data(population)

        if self.scatter is not None:
            self.scatter.remove()

        self.scatter = self.axes.scatter(x, y, z, c="r", marker="o", s=40)
        # self.canvas.draw()

    def prepare_population_data(self, population):
        x = []
        y = []
        z = []
        for p in population:
            x.append(p[0])
            y.append(p[1])
            z.append(p[2]+0.5)
        return (x, y, z)