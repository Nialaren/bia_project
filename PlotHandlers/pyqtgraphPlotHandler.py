from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
import pyqtgraph.opengl as gl

class PlotHandler(object):
    def __init__(self, parent):
        self.view = gl.GLViewWidget(parent)
        
        self.view.setCameraPosition(distance=50)
        # create three grids, add each to the view
        xgrid = gl.GLGridItem()
        ygrid = gl.GLGridItem()
        zgrid = gl.GLGridItem()

        self.view.addItem(xgrid)
        self.view.addItem(ygrid)
        self.view.addItem(zgrid)
        ## rotate x and y grids to face the correct direction
        xgrid.rotate(90, 0, 1, 0)
        ygrid.rotate(90, 1, 0, 0)

        trans = 10

        xgrid.translate(-trans,0,trans)
        ygrid.translate(0,-trans,trans)
        
        
        
        self.activePlot = None
        self.activePopulation = None

        self.surface = None
        self.scatter = None

    def get_widget(self):
        return self.view

    def updatePlot(self, X, Y, Z):
        p2 = gl.GLSurfacePlotItem(x=X, y=X, z=Z, shader='shaded')
        p2.scale(2.0, 2.0, 0.5)
        #p2.translate(0,0,-2.0)
        self.view.addItem(p2)

    def updatePopulation(self, population):
        self.activePopulation = population
        x, y, z = self.prepare_population_data(population)

        if self.scatter is not None:
            self.scatter.remove()

        self.scatter = self.axes.scatter(x, y, z, c="r", marker="o", s=40)
        self.canvas.draw()

    def prepare_population_data(self, population):
        x = []
        y = []
        z = []
        for p in population:
            x.append(p[0])
            y.append(p[1])
            z.append(p[2])
        return (x, y, z)
