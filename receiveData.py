#!/usr/bin/python3

import os
import serial 
import argparse
import time



# create parser
parser = argparse.ArgumentParser(description="Serial")
# add expected arguments
parser.add_argument('--port', dest='port', required=True)
parser.add_argument('--baud', dest='baud', required=True)
# parse args
args = parser.parse_args()
strPort = args.port
baud = args.baud

comm = serial.Serial(strPort, baud, timeout=0, xonxoff=False, rtscts=False, dsrdtr=False)



class storage:
  def __init__(self):
      
    if not os.path.exists("test.csv"):
      with open("test.csv", "a") as myfile:
        myfile.write("<TEAM ID>,<PACKET COUNT>,<ALT SENSOR>,<PRESSURE>,<SPEED>,<TEMP>,<VOLTAGE>,<GPS LATITUDE>,<GPS LONGITUDE>,<GPS ALTITUDE>,<GPS SAT NUM>,<GPS SPEED>,<COMMAND TIME>,<COMMAND COUNT>,[<BONUS>]\n")
        

  def main(self):
    while(1):
      
      
      received = comm.readline().decode('utf-8').strip('\x00')
      readings = received.split(',')
      if(received==""): 
        continue
      #TODO acknowledge
      #comm.write(("Received"+str(readings[1])).encode('utf-8'));
      with open("test.csv", "a") as myfile:
        myfile.write(received)
      line = received.split('\n')[0];
    
      print("Line = "+line)
      
      #time.sleep(1)
      #TODO cross thread communication


      
      
  def triggerFailsafe(self):
    #TODO failsafe
    print("Triggered")
  def disconnectTelemetry(self):
    #TODO disconnect
    print("Disconnected")
  def reconnectTelemetry(self):
    #TODO reconnect
    print("Reconnected")
  

if __name__=="__main__":
  store = storage()
  store.main()


