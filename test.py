#!/usr/bin/python3


from PyQt5.uic import loadUiType

import sys
import random
import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget
import numpy as np
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot
pyplot.style.use('ggplot')


    
Ui_MainWindow, QMainWindow = loadUiType('mainwindow.ui')

temperatureFigure = Figure()
velocityFigure = Figure()
pressureFigure = Figure()
altitudeFigure = Figure()


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)
        
        self.ax1f1 = temperatureFigure.add_subplot(111)
        
        self.TemperatureInCheck = True
        self.TemperatureOutCheck = True
        
        Main.addmpl(self, self.TemperatureInCheck, self.TemperatureOutCheck)
        
        
        self.inTempCheck.stateChanged.connect(self.changeTempIn)
        self.outTempCheck.stateChanged.connect(self.changeTempOut)
        
        #self.main_widget = QWidget(self)
        #l = QVBoxLayout(self.main_widget)
        #dc = MyDynamicMplCanvas(self.main_widget)
        #l.addWidget(dc)
        
    def changeTempIn(self, state):
      
        if state == QtCore.Qt.Checked:
            TemperatureInCheck = True
        else:
            TemperatureInCheck = False
        Main.updateMpl(self,  self.TemperatureInCheck, self.TemperatureOutCheck)
            
    def changeTempOut(self, state):
      
        if state == QtCore.Qt.Checked:
            TemperatureOutCheck = True
        else:
            TemperatureOutCheck = False
        Main.updateMpl(self,  self.TemperatureInCheck, self.TemperatureOutCheck)
            
            
    def updateMpl(self, inTemp, outTemp):
        
        self.ax1f1.clear()
        
        if(inTemp == True):
            self.ax1f1.plot(np.random.rand(99))
        if(outTemp == True):
            self.ax1f1.plot(np.random.rand(5))
        
        self.canvas = FigureCanvas(temperatureFigure)
        self.canvas.draw()
        
        
        ax1f2 = velocityFigure.add_subplot(111)
        ax1f2.plot(np.random.rand(9))
        ax1f2 = velocityFigure.add_subplot(111)
        ax1f2.plot(np.random.rand(9))
        self.canvas = FigureCanvas(velocityFigure)
        self.canvas.draw()
        
    def addmpl(self, inTemp, outTemp):
        
        
        if(inTemp == True):
            self.ax1f1.plot(np.random.rand(5))
        if(outTemp == True):
            self.ax1f1.plot(np.random.rand(5))
        

                
        self.canvas = FigureCanvas(temperatureFigure)
        self.temperatureLayout.addWidget(self.canvas)
        self.canvas.draw()
        
        
        ax1f2 = velocityFigure.add_subplot(111)
        ax1f2.plot(np.random.rand(9))
        ax1f2.plot(np.random.rand(9))
        self.canvas = FigureCanvas(velocityFigure)
        self.velocityLayout.addWidget(self.canvas)
        self.canvas.draw()
        
        
        ax1f2 = pressureFigure.add_subplot(111)
        ax1f2.plot(np.random.rand(15))
        self.canvas = FigureCanvas(pressureFigure)
        self.pressureLayout.addWidget(self.canvas)
        self.canvas.draw()
        
        
        ax1f2 = altitudeFigure.add_subplot(111)
        ax1f2.plot(np.random.rand(26))
        self.canvas = FigureCanvas(altitudeFigure)
        self.altitudeLayout.addWidget(self.canvas)
        self.canvas.draw()
        
        #self.toolbar = NavigationToolbar(self.canvas, 
        #        self, coordinates=True)
        #self.addToolBar(self.toolbar)
#    def setupUi(self):
#        self.main_widget = QWidget(self)
#        l = QVBoxLayout(self.main_widget)
#        dc = MyDynamicMplCanvas(self.main_widget)
#        l.addWidget(dc)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
