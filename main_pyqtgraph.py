import sys
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import testFunction as TF



class Form(QtGui.QWidget):
    def __init__(self):
        super(Form, self).__init__()
        # window settings
        #adding layout
        self.layout = QtGui.QVBoxLayout(self)
        self.setLayout(self.layout)

        self.btn = QtGui.QPushButton('change', self)
        # self.btn.clicked.connect(self.updateUI)

        self.layout.addWidget(self.btn)

        self.view = gl.GLViewWidget()
        self.layout.addWidget(self.view)
        # create our plot
        self.initializePlot()


    """
    Initialization of MathPlotLib
    - creates canvas, figure etc.
    """
    def initializePlot(self):
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
        # xgrid.scale(2,2,2)
        # ygrid.scale(2,2,2)
        # zgrid.scale(2,2,2)


        xgrid.translate(-trans,0,trans)
        ygrid.translate(0,-trans,trans)

        # grid.setDepthValue(10)  # draw grid after surfaces since they may be translucent

        #first graph


        X = np.arange(-3, 3, 0.03)
        #Basic plane
        basicPlane = np.meshgrid(X, X)

        # here choose which test plane use
        Z = TF.sineWave(basicPlane)

        p2 = gl.GLSurfacePlotItem(x=X, y=X, z=Z, shader='shaded')
        p2.scale(2.0, 2.0, 2.0)
        p2.translate(0,0,-2.0)
        self.view.addItem(p2)



    def updateUI(self):
        pass



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mw = QtGui.QMainWindow()
    mw.setWindowTitle('Project: Biologically inspired algorithms')
    mw.resize(800,800)
    cw = Form()
    mw.setCentralWidget(cw)
    mw.show()
    app.exec_()