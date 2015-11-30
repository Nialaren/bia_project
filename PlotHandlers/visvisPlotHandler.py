from PyQt4 import QtGui, QtCore
import numpy as np
import visvis as vv

app = vv.use("pyqt4")


class PlotHandler(object):
    def __init__(self, parent):
        Figure = app.GetFigureClass()
        self.figure = Figure(parent)
        # init plot
        self.axes = vv.subplot(111)
        # self.axes.axisType = "polar"
        self.activePlot = None

    def get_widget(self):
        return self.figure._widget

    def updatePlot(self, X, Y, Z):
        self.activePlot = (X,Y,Z)
        vv.clf()
        surface = vv.surf(X,Y,Z)
        surface.colormap = vv.CM_HOT

    def updateSpecimens(self, data):
        pass