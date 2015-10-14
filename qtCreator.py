 #!/usr/bin/python3


from PyQt5.uic import loadUiType
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np
from numpy import arange, sin, pi

import sys
import random

    
Ui_MainWindow, QMainWindow = loadUiType('mainwindow.ui')


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)
        fig1 = Figure()
        Main.addmpl(self, fig1)
    
    def getCanvas(self):
    
        fig = Figure()
        ax1f1 = fig.add_subplot(111)
        ax1f1.plot(np.random.rand(5))
        ax1f1 = fig.add_subplot(111)
        ax1f1.plot(np.random.rand(5))
    
        return (fig)
        
        
    def addmpl(self, layout):
        
        self.canvas = FigureCanvas(getFigure())
        self.layout.addWidget(self.canvas)
        self.canvas.draw()
        
    def updateGraphs(self):
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
