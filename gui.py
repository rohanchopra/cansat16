#!/usr/bin/python3


import sys
import subprocess

from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtGui, QtCore


Ui_MainWindow, QMainWindow = loadUiType('mainwindow.ui')

 
class MainWindow(QMainWindow, Ui_MainWindow):

  def __init__(self):
    super(MainWindow,self).__init__()
    self.setupUi(self)
    
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
    
  def connect_cansat(self):
    #subprocess.Popen("python3 receiveData.py --port /dev/", shell=True)
    pass
  def telemetry_toggle(self):
    pass
  def deploy_failsafe(self):
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
      sys.exit()
    else:
      pass
        
  def closeEvent(self, event):
    event.ignore()
    self.close_application()
    
if __name__ == '__main__':
  app = QApplication(sys.argv)
  
  GUI = MainWindow()
  GUI.show()
  sys.exit(app.exec_())
