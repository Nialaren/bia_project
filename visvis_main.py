import sys
from PyQt4 import QtGui, QtCore
import numpy as np
import visvis as vv
import testFunction as TF

# Create a visvis app instance, which wraps a qt4 application object.
# This needs to be done *before* instantiating the main window.
app = vv.use('pyqt4')

class MainWindow(QtGui.QWidget):
    def __init__(self, *args):
        QtGui.QWidget.__init__(self, *args)

        # Make a panel with a button
        self.panel = QtGui.QWidget(self)
        but = QtGui.QPushButton(self.panel)
        but.setText('Push me')

        # Make figure using "self" as a parent
        Figure = app.GetFigureClass()
        self.fig = Figure(self)

        # Make sizer and embed stuff
        self.sizer = QtGui.QHBoxLayout(self)
        self.sizer.addWidget(self.panel, 1)
        self.sizer.addWidget(self.fig._widget, 2)

        # Make callback
        # but.pressed.connect(self._Plot)

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

        # Apply sizers
        self.setLayout(self.sizer)

        # Finish
        self.resize(560, 420)
        self.setWindowTitle('Embedding in Qt pyqt4')
        self.show()


    # def _Plot(self):
    #
    #     # Make sure our figure is the active one.
    #     # If only one figure, this is not necessary.
    #     #vv.figure(self.fig.nr)
    #
    #     # Clear it
    #     vv.clf()
    #
    #     # Plot
    #     vv.plot([1,2,3,1,6])
    #     vv.legend(['this is a line'])
    #     #self.fig.DrawNow()



if __name__ == '__main__':
    qtApp = QtGui.QApplication(sys.argv)
    m = MainWindow()
    qtApp.exec_()