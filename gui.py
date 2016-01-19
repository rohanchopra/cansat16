#!/usr/bin/python3


##Approx time to plot all = 200ms
import os
import signal
import sys
import subprocess
import time
import matplotlib
import json

import zmq
from  multiprocessing import Process

matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox,QScrollArea,QHBoxLayout,QVBoxLayout,QWidget,QFrame
from PyQt5.QtCore import  QThread, pyqtSignal
from PyQt5 import QtGui, QtCore

plt.style.use('ggplot')


Ui_MainWindow, QMainWindow = loadUiType('mainwindow.ui')


    
timeValues=[]
inTemperatureValues=[]
outTemperatureValues=[]
pitotVelocityValues=[]
gpsVelocityValues=[]
pressureValues=[]
sensorAltitudeValues=[]
gpsAltitudeValues=[]





class MainWindow(QMainWindow, Ui_MainWindow):

  def __init__(self):
    super(MainWindow,self).__init__()
    self.setupUi(self)
    
    self.temperatureFig = plt.figure()
    self.velocityFig = plt.figure()
    self.altitudeFig = plt.figure()
    self.pressureFig = plt.figure()
    
    self.temperatureAxis = self.temperatureFig.add_subplot(1,1,1)
    self.velocityAxis = self.velocityFig.add_subplot(1,1,1)
    self.altitudeAxis = self.altitudeFig.add_subplot(1,1,1)
    self.pressureAxis = self.pressureFig.add_subplot(1,1,1)
    
    
    self.temperatureCanvas = FigureCanvas(self.temperatureFig)
    self.velocityCanvas = FigureCanvas(self.velocityFig)
    self.altitudeCanvas = FigureCanvas(self.altitudeFig)
    self.pressureCanvas = FigureCanvas(self.pressureFig)

 
    
    self.zmqThread = zmqWorker()
    self.zmqThread.mySignal.connect(self.print_message)
    self.zmqThread.timeSignal.connect(self.update_packetcount)
    self.zmqThread.voltageSignal.connect(self.update_voltage)
    self.zmqThread.temperatureSignal.connect(self.plot_temperature)
    self.zmqThread.velocitySignal.connect(self.plot_velocity)
    self.zmqThread.altitudeSignal.connect(self.plot_altitude)
    self.zmqThread.pressureSignal.connect(self.plot_pressure)
    
    
    
    self.temperatureLayout.addWidget(self.temperatureCanvas)
    self.velocityLayout.addWidget(self.velocityCanvas)
    self.altitudeLayout.addWidget(self.altitudeCanvas)
    self.pressureLayout.addWidget(self.pressureCanvas)
    
    self.temperatureToolbar = NavigationToolbar(self.temperatureCanvas, self)
    self.temperatureLayout.addWidget(self.temperatureToolbar)
    self.velocityToolbar = NavigationToolbar(self.velocityCanvas, self)
    self.velocityLayout.addWidget(self.velocityToolbar)
    self.altitudeToolbar = NavigationToolbar(self.altitudeCanvas, self)
    self.altitudeLayout.addWidget(self.altitudeToolbar)
    self.pressureToolbar = NavigationToolbar(self.pressureCanvas, self)
    self.pressureLayout.addWidget(self.pressureToolbar)
    
    
    
    
    self.workerThread = Test()
    self.workerThread.mySignal.connect(self.on_change)
    
    self.portEdit.setText('/dev/ttyACM5')
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
    
  #check if plot corresponding to check box correct
  def plot_temperature(self,temp):
    #TODO update only last point?
    
    self.temperatureAxis.clear()
    
    if(int(timeValues[-1])<10):
      self.temperatureAxis.set_xlim(0,10)
    else:
      self.temperatureAxis.set_xlim(int(timeValues[-1])-10,int(timeValues[-1]))
    self.temperatureAxis.set_ylim(0,50)
    
    if(self.inTempCheck.isChecked()==True):
      self.temperatureAxis.plot(timeValues, inTemperatureValues,c='r')
    if(self.outTempCheck.isChecked()==True):
      self.temperatureAxis.plot(timeValues, outTemperatureValues,c='b')
    self.temperatureCanvas.draw()
    
  def plot_velocity(self,velocity):
    #TODO update only last point?
    
    self.velocityAxis.clear()
    
    if(int(timeValues[-1])<10):
      self.velocityAxis.set_xlim(0,10)
    else:
      self.velocityAxis.set_xlim(int(timeValues[-1])-10,int(timeValues[-1]))
    self.velocityAxis.set_ylim(0,100)
    
    if(self.pitotVelocityCheck.isChecked()==True):
      self.velocityAxis.plot(timeValues, pitotVelocityValues,c='r')
    if(self.gpsVelocityCheck.isChecked()==True):
      self.velocityAxis.plot(timeValues, gpsVelocityValues,c='b')
    self.velocityCanvas.draw()
    
  def plot_altitude(self,alt):
    #TODO update only last point?
    
    self.altitudeAxis.clear()
    
    if(int(timeValues[-1])<10):
      self.altitudeAxis.set_xlim(0,10)
    else:
      self.altitudeAxis.set_xlim(int(timeValues[-1])-10,int(timeValues[-1]))
    self.altitudeAxis.set_ylim(0,1000)
    
    if(self.sensorAltitudeCheck.isChecked()==True):
      self.altitudeAxis.plot(timeValues, sensorAltitudeValues,c='r')
    if(self.gpsAltitudeCheck.isChecked()==True):
      self.altitudeAxis.plot(timeValues, gpsAltitudeValues,c='b')
    self.altitudeCanvas.draw()
    #millis = int(round(time.time() * 1000))
    #print("t3:")
    #print (millis)
  def plot_pressure(self,pressure):
    #TODO update only last point?
    
    self.pressureAxis.clear()
    
    if(int(timeValues[-1])<10):
      self.pressureAxis.set_xlim(0,10)
    else:
      self.pressureAxis.set_xlim(int(timeValues[-1])-10,int(timeValues[-1]))
    self.pressureAxis.set_ylim(0,1000)
    
    self.pressureAxis.plot(timeValues, pressureValues,c='r')
    self.pressureCanvas.draw()
    
    
  def update_packetcount(self,time):
    self.missionTimeText.setText(time)
    
  def update_voltage(self,voltage):
    self.voltageText.setText(voltage)
  
  def print_message(self,text):
    print(text)
  
  def on_change(self,text):
    global xs
    global ys
    print("Done!"+text+xs[0]+ys[0])
    
    
   
    self.temperatureAxis.clear()
    self.temperatureAxis.plot(xs, ys)
    self.temperatureAxis.plot(ys, xs)
    print(xs)
    self.temperatureCanvas.draw()
    
    
    
  def connect_cansat(self):
    #better check for multiple clicks
    self.connectButton.setEnabled(False)
    port = self.portEdit.text()
    baud = self.baudRateEdit.text()
    
    self.pro = subprocess.Popen("python3 receiveData.py --port "+port+" --baud "+baud, shell=True,preexec_fn=os.setsid)
    self.zmqThread.start()
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
  
    #TODO fix:close before connect hangs
    choice = QMessageBox.question(self, 'Quit?',
                                              "Quit the GCS?",
                                              QMessageBox.Yes | QMessageBox.No)
    if choice == QMessageBox.Yes:
      self.zmqThread.start()    #Why do you need to start thread to properly exit app
      try:
        os.killpg(self.pro.pid, signal.SIGTERM)
        
      except:
        pass
      print("Exiting")
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
    xz = []
    yz = []
    global ax1
    for line in lines:
      if len(line) > 1:
        x, y = line.split(',')
        xz.append(x)
        yz.append(y)
    xs = xz
    ys = yz
    self.mySignal.emit("update")
    
    
class zmqWorker(QThread):
  
  mySignal = pyqtSignal(str) 
  timeSignal = pyqtSignal(str)
  voltageSignal = pyqtSignal(str)
  temperatureSignal = pyqtSignal(str)
  velocitySignal = pyqtSignal(str)
  altitudeSignal = pyqtSignal(str)
  pressureSignal = pyqtSignal(str)
  def __init__(self):
      super().__init__()
      
      # Initialize a zeromq context
      context = zmq.Context()

      # Set up a channel to receive work from the ventilator
      self.work_receiver = context.socket(zmq.REQ)
      self.work_receiver.bind('tcp://127.0.0.1:5540')

  def run(self):
    while True:
      #millis = int(round(time.time() * 1000))
      #print("t1:")
      #print (millis)
      self.work_receiver.send('1'.encode("utf-8"))
      work_message = self.work_receiver.recv()  
      decoded = json.loads(work_message.decode("utf-8"))
      
      timeValues.append(decoded["PacketCount"])
      
      inTemperatureValues.append(decoded["Temp"])
      outTemperatureValues.append(decoded["GPSSatNum"])
      
      pitotVelocityValues.append(decoded["Speed"])
      gpsVelocityValues.append(decoded["GPSSpeed"])
      
      sensorAltitudeValues.append(decoded["AltSensor"])
      gpsAltitudeValues.append(decoded["GPSAltitude"])
      
      pressureValues.append(decoded["Pressure"])
      
      self.temperatureSignal.emit(decoded["Temp"])
      self.velocitySignal.emit(decoded["Speed"])
      self.altitudeSignal.emit(decoded["AltSensor"])
      self.pressureSignal.emit(decoded["Pressure"])
      
      
      self.timeSignal.emit(decoded["PacketCount"])
      #self.mySignal.emit(work_message.decode("utf-8"))
      self.voltageSignal.emit(decoded["Voltage"])
      #millis = int(round(time.time() * 1000))
      #print("t2:")
      #print (millis)

if __name__ == '__main__':
  app = QApplication(sys.argv)
  
  GUI = MainWindow()
  
  GUI.show()
  sys.exit(app.exec_())
