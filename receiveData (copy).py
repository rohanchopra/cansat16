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
    #self.ventilator_send.connect('tcp://127.0.0.1:5540')
    
    if not os.path.exists("test.csv"):
      with open("test.csv", "a") as myfile:
        myfile.write("<TEAM ID>,<PACKET COUNT>,<ALT SENSOR>,<PRESSURE>,<SPEED>,<TEMP>,<VOLTAGE>,<GPS LATITUDE>,<GPS LONGITUDE>,<GPS ALTITUDE>,<GPS SAT NUM>,<GPS SPEED>,<COMMAND TIME>,<COMMAND COUNT>,[<BONUS>]\n")
        

  def main(self):
  
    flag=0
    x=[]
    receive=[]
    while(1):
      time.sleep(1)
      try:
        global line
        #received=""
        while 1:
          time.sleep(1)
          comm.flush()
          receive = comm.readline().rstrip()#decode('utf-8').strip('\x00')
         # print(receive)
          #if "\n" in receive:
           # received = received + receive.split('\n')[0]
            #break
          #received = received + receive
        #received = received.split('\r')[0]  
        #readings = received.split(',')
        #print(received+"\n")
          if(receive):
             x=receive.split('S')
             #print x
             #print(receive.split('S'))
             for i in x:
                #print i
                if(len(i)==85):
                    print i
                    #TODO acknowledge
                    #comm.write(("Received"+str(readings[1])).encode('utf-8'));
                    with open("final.csv", "a") as myfile:
                        myfile.write(i+'\n')
                    #line = 
                    print(readings[1])
                    #handling arduino uno reset remove when capacitor available
                    if(flag==0 and int(readings[1])==1):
                        flag=1
                    if(flag==0):
                        continue

                    print(line)
                    jsonReadings = {}
                    jsonReadings["flag"] = readings[0]
                    jsonReadings["TeamID"] = readings[1]
                    jsonReadings["MissionTime"] = readings[2]
                    jsonReadings["PacketCount"] = readings[3]
                    jsonReadings["AltSensor"] = readings[4]
                    jsonReadings["Pressure"] = readings[5]
                    jsonReadings["Speed"] = readings[6]
                    jsonReadings["InTemp"] = readings[7]
                    jsonReadings["Voltage"] = readings[8]
                    jsonReadings["GPSLatitude"] = readings[9]
                    jsonReadings["GPSLatChar"] = readings[10]
                    jsonReadings["GPSLongitude"] = readings[11]
                    jsonReadings["GPSLonChar"] = readings[12]
                    jsonReadings["GPSAltitude"] = readings[13]
                    jsonReadings["GPSSatNum"] = readings[14]
                    jsonReadings["GPSSpeed"] = readings[15]
                    jsonReadings["LastCommandTime"] = readings[16]
                    jsonReadings["CommandCount"] = readings[17]
                    jsonReadings["State"] = readings[18]
                    jsonReadings["OutTemp"] = readings[19]
                    jsonReadings["flag2"] = readings[20] 
        
                    json_data = json.dumps(jsonReadings)
       
                    msg = self.ventilator_send.recv()
        
                    self.ventilator_send.send(json_data.encode("utf-8"))

        """if(received==""): 
          continue
        if(line==received):
          continue
        if(readings[1]!='1001'): #TODO change to team id
          continue
        print(readings[0]+"   "+readings[20])
        if(readings[0]!=reading[20]!='seds'): #TODO check
          continue"""
                
        
        
        
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
  def capture(self):
    print("Capture Command Sent")
 
if __name__=="__main__":
  store = storage()
  store.main()


