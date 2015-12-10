from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np

class PlotHandler(object):
    def __init__(self, parent):
        self.figure = Figure(tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setContentsMargins(0,0,0,0)
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
        x, y = np.meshgrid(X,Y)

        if self.surface is not None:
            self.surface.remove()

        self.surface = Axes3D.plot_surface(self.axes, x, y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False, shade=False, alpha=0.5)
        self.canvas.draw()

    def updatePopulation(self, population):
        self.activePopulation = population
        x, y, z = self.preparePopulationData(population)

        if self.scatter is not None:
            self.scatter.remove()

        self.scatter = Axes3D.scatter(self.axes, x, y, z, c="r", marker="o", s=40)
        self.surface.set_zorder(2)
        self.scatter.set_zorder(100)
        self.scatter.set_alpha(1.0)
        self.canvas.draw()

    def preparePopulationData(self, population):
        x = []
        y = []
        z = []
        for p in population:
            # x.append(p.parameters[0])
            # y.append(p.parameters[1])
            # z.append(p.fitness)
            x.append(p[0])
            y.append(p[1])
            z.append(p[2])
        return (x, y, z)
