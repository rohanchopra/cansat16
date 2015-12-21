#!/usr/bin/python3

import os
import serial 
import json
import sys
import argparse
import time

import zmq
from  multiprocessing import Process


# create parser
parser = argparse.ArgumentParser(description="Serial")
# add expected arguments
parser.add_argument('--port', dest='port', required=True)
parser.add_argument('--baud', dest='baud', required=True)
# parse args
args = parser.parse_args()
strPort = args.port
strbaud = args.baud
try:
  comm = serial.Serial(strPort, strbaud, timeout=0, xonxoff=False, rtscts=False, dsrdtr=False)
except:
  print("Bad port")
  sys.exit()
print ("baud = "+strbaud+"\nport = "+strPort+"\nStarted Receiving")
line = ""
class storage:
  def __init__(self):
      
    # Initialize a zeromq context
    self.context = zmq.Context()
 
    # Set up a channel to send work
    self.ventilator_send = self.context.socket(zmq.REP)
    self.ventilator_send.bind('tcp://127.0.0.1:5552')
    
    if not os.path.exists("test.csv"):
      with open("test.csv", "a") as myfile:
        myfile.write("<TEAM ID>,<PACKET COUNT>,<ALT SENSOR>,<PRESSURE>,<SPEED>,<TEMP>,<VOLTAGE>,<GPS LATITUDE>,<GPS LONGITUDE>,<GPS ALTITUDE>,<GPS SAT NUM>,<GPS SPEED>,<COMMAND TIME>,<COMMAND COUNT>,[<BONUS>]\n")
        

  def main(self):
  
  
    while(1):
      try:
        global line
        received=""
        while 1:
          receive = comm.readline().decode('utf-8').strip('\x00')
          if "\n" in receive:
            received = received + receive.split('\n')[0]
            break
          received = received + receive
        received = received.split('\r')[0]  
        readings = received.split(',')
        if(received==""): 
          continue
        if(line==received):
          continue
        if(readings[0]!='132'):
          continue
        #TODO acknowledge
        #comm.write(("Received"+str(readings[1])).encode('utf-8'));
        with open("test.csv", "a") as myfile:
          myfile.write(received)
        line = received
        
      
        #print("Line = "+line)
        
       
        #TODO cross thread communication
        
        jsonReadings = {}
        jsonReadings["TeamID"] = readings[0]
        jsonReadings["PacketCount"] = readings[1]
        jsonReadings["AltSensor"] = readings[2]
        jsonReadings["Pressure"] = readings[3]
        jsonReadings["Speed"] = readings[4]
        jsonReadings["Temp"] = readings[5]
        jsonReadings["Voltage"] = readings[6]
        jsonReadings["GPSLatitude"] = readings[7]
        jsonReadings["GPSLongitude"] = readings[8]
        jsonReadings["GPSAltitude"] = readings[9]
        jsonReadings["GPSSatNum"] = readings[10]
        jsonReadings["GPSSpeed"] = readings[11]
        jsonReadings["CommandTime"] = readings[12]
        jsonReadings["CommandCount"] = readings[13]
         
        json_data = json.dumps(jsonReadings)
        
       
        msg = self.ventilator_send.recv()
        self.ventilator_send.send(json_data.encode("utf-8"))
        
        
        
        time.sleep(0.5)
      except:
        pass
      
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


