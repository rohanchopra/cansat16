#!/usr/bin/python3

import os
import signal
import sys
import subprocess
import time
import matplotlib

import zmq
from  multiprocessing import Process

matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import  QThread, pyqtSignal
from PyQt5 import QtGui, QtCore


Ui_MainWindow, QMainWindow = loadUiType('mainwindow.ui')


    
xs=[]
ys=[] 




class MainWindow(QMainWindow, Ui_MainWindow):

  def __init__(self):
    super(MainWindow,self).__init__()
    self.setupUi(self)
    self.fig = plt.figure()
    self.ax1 = self.fig.add_subplot(1,1,1)
    self.canvas = FigureCanvas(self.fig)
    
    
 
    
    self.zmqThread = zmqWorker()
    self.zmqThread.mySignal.connect(self.print_message)
    
    
    
    #self.temperatureLayout.addWidget(self.canvas)
    
    
    self.workerThread = Test()
    self.workerThread.mySignal.connect(self.on_change)
    
    self.portEdit.setText('/dev/ttyACM0')
    self.baudRateEdit.setText('9600')
    self.failsafeCheck.stateChanged.connect(self.fail_safe)
    self.connectButton.clicked.connect(self.connect_cansat)
    self.telemetryButton.clicked.connect(self.telemetry_toggle)
    self.failsafeButton.clicked.connect(self.deploy_failsafe)
    self.inTempCheck.stateChanged.connect(self.in_temp)
    self.outTempCheck.stateChanged.connect(self.out_temp)
    self.pitotVelocityCheck.stateChanged.connect(self.pitot_velocity)
    self.gpsVelocityCheck.stateChanged.connect(self.gps_velocity)
    self.sensorAltitudeCheck.stateChanged.connect(self.sensor_altitude)
    self.gpsAltitudeCheck.stateChanged.connect(self.gps_altitude)
    
  def print_message(self,text):
    print(text)
  
  def on_change(self,text):
    global xs
    global ys
    print("Done!"+text+xs[0]+ys[0])
    self.ax1.clear()
    self.canvas.draw()
    self.ax1.plot(xs, ys)
    self.ax1.plot(ys, xs)
    self.canvas.draw()
    
  def connect_cansat(self):
    port = self.portEdit.text()
    baud = self.baudRateEdit.text()
    self.pro = subprocess.Popen("python3 receiveData.py --port "+port+" --baud "+baud, shell=True)
    self.zmqThread.start()
    #subprocess.Popen("python3 iprint.py", shell=True)
    pass
  def telemetry_toggle(self):
    self.workerThread.start()
    pass
  def deploy_failsafe(self):
    self.workerThread.terminate()
    pass
  def in_temp(self):
    pass
  def out_temp(self):
    pass
  def pitot_velocity(self):
    pass
  def gps_velocity(self):
    pass
  def sensor_altitude(self):
    pass
  def gps_altitude(self):
    pass
    
  def fail_safe(self):
    if(self.failsafeButton.isEnabled()==False):
      self.failsafeButton.setEnabled(True)
    else:
      self.failsafeButton.setEnabled(False)
  
  
  def close_application(self):
  
    choice = QMessageBox.question(self, 'Quit?',
                                              "Quit the GCS?",
                                              QMessageBox.Yes | QMessageBox.No)
    if choice == QMessageBox.Yes:
      print("Exiting")
      #work_receiver.close()
      #context.Term()
      #self.results_sender.close()
      #zmq_ctx_destroy()
      sys.exit()
    else:
      pass
        
  def closeEvent(self, event):
    event.ignore()
    self.close_application()
   
class Test(QThread):
  
  mySignal = pyqtSignal(str) 
  def __init__(self):
      super().__init__()

  def run(self):
    
    graph_data = open('samplefile.txt','r').read()
    lines = graph_data.split('\n')
    global xs
    global ys
    global ax1
    for line in lines:
      if len(line) > 1:
        x, y = line.split(',')
        xs.append(x)
        ys.append(y)
    
    self.mySignal.emit("update")
    
    
class zmqWorker(QThread):
  
  mySignal = pyqtSignal(str) 
  def __init__(self):
      super().__init__()
      
      # Initialize a zeromq context
      context = zmq.Context()

      # Set up a channel to receive work from the ventilator
      self.work_receiver = context.socket(zmq.REQ)
      self.work_receiver.connect('tcp://127.0.0.1:5547')

  def run(self):
    while True:
      self.work_receiver.send('1'.encode("utf-8"))
      work_message = self.work_receiver.recv()    
      self.mySignal.emit(work_message.decode("utf-8"))
    
  def __del__(self):
      print("here")
      self.work_receiver.close()
      self.context.term()
      #context.Term()
if __name__ == '__main__':
  app = QApplication(sys.argv)
  
  GUI = MainWindow()
  
  GUI.show()
  sys.exit(app.exec_())
