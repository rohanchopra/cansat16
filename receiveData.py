#!/usr/bin/python3

import os
import serial 
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
    self.ventilator_send.bind('tcp://127.0.0.1:5547')
    
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
        #line = received.split('\n')[0];
      
        #print("Line = "+line)
        
       
        #TODO cross thread communication
        
       
        msg = self.ventilator_send.recv()
        self.ventilator_send.send(line.encode("utf-8"))
        
        
        
        time.sleep(0.5)
      except:
        self.ventilator_send.close()
        #self.context.Term()
      
  def triggerFailsafe(self):
    #TODO failsafe
    print("Triggered")
  def disconnectTelemetry(self):
    #TODO disconnect
    print("Disconnected")
  def reconnectTelemetry(self):
    #TODO reconnect
    print("Reconnected")
  
  def __del__(self):
    self.ventilator_send.close()
    self.context.term()

if __name__=="__main__":
  store = storage()
  store.main()


